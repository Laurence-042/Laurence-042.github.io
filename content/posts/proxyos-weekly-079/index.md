+++
date = '2026-07-24T10:07:00+08:00'
draft = false
title = 'Proxyos Weekly 079'
slug = 'proxyos-weekly-079'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> mod化迁移后的核心数据已经跑通，接下来就是枯燥的测试工作了

{{< toc >}}

# 本期目标

- [ ] 修 bug
  - [ ] mod 数据加载
    - [ ] overlay 合并
    - [x] 网页 route
  - [x] 基于 SpiderView 的 mod 自定义 AppView 冒烟
  - [ ] 文件引用处理冒烟
- [ ] 将第三章开头补充进 demo
  - [ ] 调整第二章末尾文本，引入经济系统和支线任务系统
  - [ ] 通过经济系统获得通用搭载平台
  - [ ] 将 demo 结束提示放在通用搭载平台的 app 里（SpiderView 实现）
- [ ] 更多内容
  - [ ] 支线任务
  - [ ] 更多任务
  - [ ] 实用化任务时限
  - [ ] 命令行内容？（等第三章？是否需要？）
  - [ ] 远程访问？
  - [ ] 更精细化管理事件而不是按章组织？mod 支持？
- [ ] 用英语通玩一遍
- [ ] 开个 itch
- [ ] 琢磨下宣传

# 进展速记

## 本期假设 / 预期

**预期：**

上期暴露了剧本数据无法正常加载的 bug，这期核心是修好它，然后能做多少做多少

**结果：**

修好了剧本数据的 bug，现在游戏能正常启动，正常加载，正常运行了。至少核心技术都通了，接下来就是一次冒烟通跑了

## 本期确定性变化

### 新增：

- 添加了一批调试日志，便于跟踪
- 现在日志会同步输出到单独的文件，不会被 godot 的日志输出限流截断了
- 

### 变更：

- 优化剧本系统 serde 架构，使其更易维护
- 优化任务详情界面中的任务需求展示，现在它们不会叠在一起或者撑出水平滚动条了

### 修复：

- 修复 mod 里剧本数据无法正常起效的 bug
- 修复剧本中部分触发器、动作因为 int 入参被 Godot 的 JSON.parse_string 解释成了 float 而出现偏差的 bug
- 修复之前改 Godot-wry 时改坏的 res 协议处理

### 删除：

- 移除了基于 class_name 标记的 serde 特性，现在都要走显式类型指定

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## yaml 竟然出问题了……

| # | 问题 | 根因 | 修复 |
| :--- | :--- | :--- | :--- |
| 1 （根因） | story 事件全部 on_conditions=0，挂上不触发 | PyYAML safe_load 走 YAML 1.1，把 on: 键解析成布尔 True，data.get("on") 取不到 → 条件没编译进事件 | 新增 yaml_loader.py（YAML 1.2 core schema，on/off/yes/no 保持字符串），3 处 YAML 读取改用它 |
| 2 | load_yaml failed for condition 'time_advanced' | time_advanced: 0 是合法值（文档："留 0 表示任意休眠均触发"），但 load_yaml 写了 return after_game_ms > 0 把 0 当非法 | 改为 return true（任何可解析整数都合法，0=任意） |
| 3 | 未找到任务定义：-1_transfer | _revalidate_active_tasks() 在 _on_app_ready 里跑，此时 framework_ready.pocket 还没加载 mod 任务定义 → 查不到 | 从 _on_app_ready 移除，改到 MainSceneLoader 的 scan_and_activate_tasks() 之后（此时定义+章节条件都已就绪） |

 #2、#3 之前不发作，正是因为 #1 让所有事件变哑的——-1_transfer 从来没被 issue 成 ACTIVE，自然没有 ACTIVE
 任务需要重校验。这说明 story/task 事件系统之前从未真正端到端跑通过。

我是真没想到我按照编程规范用 pyyaml、用 safe_load，结果反而被 yaml 1.1 坑了，这谁知道还有这特性啊……

> 这进一步坚定了我 json 派的立场

## Codex 仍然在出问题……

### 服务中断

干一半，OpenAI 不知道搞啥子突然调不通了，然后看了下 https://downdetector.com/status/openai/，果然炸了

然后恢复后给我整的逻辑看得极其割裂，但讽刺的是，我甚至不能确定这是 OpenAI 挂掉导致的上下文断裂，还是 Codex 又在一如既往地犯蠢

Codex 也算是在出问题这方面从没让人失望过了

### 屎一样的理解力和长对话管理

如下是一个对话摘要

Q：（甩报错 StackTrace）

A：YAML 里的 `0` 在 Python 端确实是 `int`，但它作为资源目录中的无结构 `Variant` 穿过 JSON/WebSocket 后，Godot 得到的是 `float(0.0)`。这个剧本对象因为在预期得到 int 的时候得到 float 而报错。我把它改成能接受 2.999、1.0 这样的 float 了

Q：为什么经过 ipc 会变成 0.0？ipc 只是个 websocket，是发送侧有问题还是接收侧有问题？不论是哪个有问题都不该在这地方做专门 patch 吧，这明显是个底层机制无法区分 int 和 float 的底层问题

A：对，WebSocket 没问题。丢失发生在 Godot 接收侧：`JSON.parse_string()` 将所有 number 用 `String::to_float()` 解析。JSON 标准本身也只有 number，没有 int/float 类型区分。我把专用兼容回退了，然后在 IPC 接收侧写了个递归修复。

Q：我如果我理解没错，这个应该做进 serde，而不是单独一个 ipc patch

A：做了，我要求 mod 侧使用`_INTEGER_MARKER_BASE`标记整数，来让 godot 侧的 serde 能正常反序列化

Q：你给我重新做计划，这_INTEGER_MARKER_BASE 本身我看都不是必要的，这本质上就是一个给递归 parser 里 parse number 的部分加个 integer 保护，你 tm 在这整啥呢

A：对，之前方案绕远了。我需要做如下 6 个修改面……

Q：我血压要爆了，理论上你就改一下 scenes\proxy_os\json\serializable_serde.gd 的_coerce_primitive 就完事，给我对照 git 记录把你拉的屎清了然后好好做

A：完成了，我 git reset 后发现 mod 侧发的是就是 0，所以我把之前的剧本对象校验整个删了。

Q：你这个是不是矛盾了？如果 mod 侧发的是 int，godot 侧接的是 int，serde 后还是 int，那 TimeAdvancedCondition 检查 int 不该失败啊，你改 TimeAdvancedCondition 难道不是掩盖问题吗？我要一份完整报告

A：不矛盾，因为“Godot 侧接到的是 int”这个前提不成立。Godot 的 JSON.parse 会把 json string 里的 0 读成 float，然后 serde 才能根据对象类型将其恢复。

Q：那问题就是不该用 JSON.parse，而是应该使用 JsonSerializer.parse。我印象里 python 读 yaml 都出来的是能区分 1 和 1.0 的，而其 json serialize 应该也能分别写成 1 和 1.0，那么 JsonSerializer.parse 就应该能正常区分两者

A：对，你是对的。我之前把“JSON 语义只有 number”错误地等同成了“解析器无法保留词法类型”。我在 JsonSerializer 里加了一个完整 JSON Token Parser……

Q：你给我等下，我们需要讨论一下。你实现的这个和 SerializableSerde 的差异是什么

A：两者不是同一层，职责正好前后相接，JsonSerializer 处理 string 到 dict，SerializableSerde 处理 dict 到具体 object

Q：那我觉得这说明 SerializableSerde 缺少 string-dict 转换功能，parser 需要写在它里面。因为 JsonSerializer 本质上是个对接不同 serde 的适配器

A：（把 JsonSerializer 改成了 abstract，然后让 SerializableSerde 继承它，完全忽略了 JsonSerializer 始终在调 SerializableSerde、本质上是不同 serde 的适配层的事实，并且即将把所有对 JsonSerializer 的调用改成对 SerializableSerde 的调用）

Q：（愤怒地终止 agent 并 git reset）

## Godot-WRY被我改挂了

倒不是把上游仓库搞挂了，是我个人仓库

我之前看到有这么段代码

```rust
    #[func]
    fn load_url(&self, url: GString) {
        let mut url_str = String::from(url);

        if let Some(stripped) = url_str.strip_prefix("res://") {
            let path = stripped.replace("\\", "/");
            
            #[cfg(target_os = "linux")]
            {
                url_str = format!("res://{}", path);
            }

            #[cfg(not(target_os = "linux"))]
            {
                url_str = format!("http://res.{}", path);
            }
        }

        if let Some(webview) = &self.webview {
            let _ = webview.load_url(&url_str);
        }
    }
```

从git记录上看，最近的修改是一位开发者添加了linux的处理块。

然后我就想当然地觉得使用`"http://res.{}"`纯粹是之前写的时候没实现好，毕竟`build_webview`的时候都用`with_custom_protocol`注册`res`协议了，于是我直接改成全用`"res://{}"`了。

然后就炸了。

事实证明，windows的webview确实只接受这种转义后的结果。

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- mod meta、mod list、pylock.toml、依赖安装与版本回滚之间还需要形成稳定流程，否则后续 mod 管理会变成新的技术债。
  

# 下期计划

- [ ] 修 bug
  - [ ] mod 数据加载
    - [ ] overlay 合并
  - [ ] 文件引用处理冒烟
- [ ] 将第三章开头补充进 demo
  - [ ] 调整第二章末尾文本，引入经济系统和支线任务系统
  - [ ] 通过经济系统获得通用搭载平台
  - [ ] 将 demo 结束提示放在通用搭载平台的 app 里（SpiderView 实现）
- [ ] 更多内容
  - [ ] 支线任务
  - [ ] 更多任务
  - [ ] 实用化任务时限
  - [ ] 命令行内容？（等第三章？是否需要？）
  - [ ] 远程访问？
  - [ ] 更精细化管理事件而不是按章组织？mod 支持？
- [ ] 用英语通玩一遍
- [ ] 开个 itch
- [ ] 琢磨下宣传

# 试玩版

暂缓，第一次上传需要做好准备，等进入 beta 阶段再说