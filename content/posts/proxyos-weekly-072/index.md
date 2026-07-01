+++
date = '2026-06-29T11:07:00+08:00'
draft = false
title = 'Proxyos Weekly 072'
slug = 'proxyos-weekly-072'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 桌宠系统和信息段系统都已 mod 化，剧本系统 mod 化完成了初步规划，清理了技术债，确定了 codex 交互范式

{{< toc >}}

# 本期目标

- [ ] 支线任务支持
  - [x] 桌宠系统 mod 化
  - [x] 信息段系统 mod 化
  - [ ] 剧本系统 mod 化
- [x] 清技术债
  - [x] lesson-runner 的 step 处理逻辑应该在 step 里，而不是在 lesson-runner 里
  - [x] 其他发现的
- [ ] 迁移现有内容中适合 mod 化的部分（基本是完整第二章）
- [ ] 将第三章开头补充进 demo
  - [ ] 调整第二章末尾文本，引入经济系统和支线任务系统
  - [ ] 通过经济系统获得通用搭载平台
  - [ ] 将 demo 结束提示放在通用搭载平台的 app 里
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

这期因为家里一些事可能导致休息不佳导致效率下降，而且也只有 2 工作日

我想优先搞定技术债清理，然后把 mod 化的架构搭完，这样下期我就能迁移现有内容，然后考虑把第三章开头写了

**结果：**

效率确实骨折了，作息直接乱套，三天都没进入工作状态，但也没进入休息状态，以至于只是做了些没有太大决策空间的技术债优化以及桌宠、信息段的 mod 化——倒是和预期一致

mod 架构基本确定了，但是我想等下期彻底完成 mod 能力后再详细说明。这期我只简单提一嘴流程，然后聚焦于下期要做的 mod 的最后一部分——也就是 mod 化剧本的初步设计

## 本期确定性变化

### 新增：

- 桌宠系统 mod 化
- 信息段系统 mod 化

### 变更：

- 规范化 json serde 处理以及接口定义，之前没注意 codex 写的 tmd 是把所有需要序列化的类显式写序列化器里了……血压 UP
  - to_json_value()
  - from_json_value()
  - to_json_string()
  - from_json_string()
- 规范化 mod 加载
- 给 codex 擦屁股，优化前后端请求数据结构，精简字段
- 给 codex 擦屁股，购物的 hook 后效不该随购物消息传到 godot 侧，而是应该让 hook handler 自己去调 sdk
- 给 codex 擦屁股，把到处都是的 url 解析抽取为 helper
- 给 codex 擦屁股，优化交易架构，让付款处理服务在付款成功后回调电商后端的回调不再是单独命令，而是作为 merchant 的一部分注册，然后由对应的 handler 处理
- 优化第一章的 LessonRunner，将其 Step 的执行逻辑分散到 LessonStep 里，而不是像之前一样全塞在 LessonRunner 里
- 扩展 godot 侧的网页后端，使其支持其他 scheme
- 将游戏里的内置核心后端使用不同于 proxy://的 cpg:// scheme，使其在 lore 和开发上都明确定位
- 优化桌宠系统数据结构，现在只有一个数据结构，没有按文本临时拼的模式了

### 修复：

- 修复了不同 mod 提供的不同 merchant 的 sku 可能会撞的 bug，不同 mod 仍被允许使用相同 merchant 来扩充商品类型
- 修复了后端路径泄露到前端的 bug

### 删除：

- 移除 trigger_type，当时架构调整有了更好的 Trigger 备注机制后没删干净

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## coedx 的稳定交互范式

经尝试，codex 其实还是可以用的，只是需要注意很多东西：

不管让它干啥，就算只是挪个文件，也要求它先 plan 模式，否则必定歪

一次对话里只干一件事，不要在一个对话里依次干多件事

将任务粒度分得更细，避免让 codex 同时处理涉及多个系统变更的任务。宁可这次写完后续返工，也不要让它同时横跨多个系统做联动修改，否则它工作的可靠性会暴跌

## mod 加载流程概述

1. godot 以最小依赖 launch mod_manager（由 python_embed 自带依赖处理）
2. mod_manager 处理 about 扫描
3. mod_manager 找下 mod_list.txt，没找到就把 Core 视为激活 mod（需要注意这个需要用 list 存储常量，以后可能会出以 Mod 形式提供的官方 dlc）
4. mod_manager 备份 Mods 目录下旧的 pyproject.toml 和 venv，把 mod_list.txt 里激活的 mod 的目录都视为 Mods 总项目的子项目，用 uv 生成 Mods 总项目的 pyproject.toml（总引用），然后通过 [tool.uv.workspace] 引用激活 mod 的配置，最后通过 uv 完成 Mods 下新 venv 的所需的依赖安装。如果出错了就直接爆出来并终止流程，让用户处理 mod 依赖不兼容
5. mod_manager 通过 venv launch _framework\main.py 并传入 mod 顺序，main 根据 mod 顺序做 mod 加载，让各个 component 按顺序加载 mod。如果期间出错了就跳过 mod 继续加载，最后给出 mod 加载状态，并提示可能有些 mod 内容只有部分被加载，建议玩家处理 
6. main 报 framework_ready

## 剧本系统 mod 化

### 背景
目前这个游戏有一套基于 DAG 的 Event-Trigger-Action 剧本编排系统。我的游戏剧本本质上是一个以任务为核心的事件导向系统。任务之间的依赖关系保证任务的激活顺序，任务激活、发放、完成 都有对应的 Trigger 钩子用于触发 发送消息、发放奖励、设置相关数据 的 Actions

其核心理念是，每个 Event 都是一个节点，边则是节点之间的依赖。一个 Event 只有在“并非所有入边相连的 Event 都未执行过”时才能激活，而一个 Event 在激活后就可以根据其内部配置的 Trigger 触发其内部的 Actions 序列产生一系列动作

并且 Event 系统和 Task 系统解耦，Event 主要由 Task 驱动，但也可以由包括但不限于 信息段解锁、消息被阅读、通知被确认 等等动作驱动

为了保证整个系统可维护，我使用了强类型的枚举式 Trigger，并通过 Godot 的 tres 编辑器指定类型的方式来保证类型正确、数据关系可追踪。后来为了灵活性引入了 DAG 机制，其实 DAG 本质上就是承担 and、or 等条件表达式的功能

但既然要做 mod 友好的范式迁移，直接让 mod 作者写这个剧本编排系统的数据结构恐怕就十分反人类（即便 Mod 作者的预期技术水平是会写点脚本，因为本质上 mod 的核心是提供游戏世界里的网站和网站 rest api handler）

### 大致计划

使用类似下面的方式注册 Trigger、Action
```python
const SCHEMA := {
    "type": "message_viewed",
    "params": {
        "sender": {
            "type": "string",
            "default": "",
            "required": false,
        },
        "message_id": {
            "type": "string",
            "default": "",
            "required": false,
        },
    }
}
```

然后 Mod 侧使用下面的文件格式定义行为

```yaml
# quest_investigate_leak.yaml
meta:
  id: investigate_leak
  name: "调查数据泄露"
  version: 1

events:
  # 一个 event 就是一个任务节点
  - id: receive_tip
    name: "收到匿名线报"
    # 依赖：DAG 的入边。支持结构化布尔表达式
    # enabled_if 判断事件是否进入监听状态
    # 在启动时、任意 event 被执行后进行重新检查
    enabled_if:
      all:
        # 完成过事件
        - event: game_start
        # 完成过任务
        - task: some_task_id
        # 设置过标志位
        - flag: tutorial_done
    # 激活 / 发放 / 完成 各阶段的 trigger -> actions
    # on 判断事件进入监听状态后，什么运行时信号会触发 actions。
    on:
      # 多参数场景使用单键字典
      - message_viewed: {sender: "cybertaoism", message_id: "foobar"}
    # 进入监听状态后 on 被触发后执行的 actions。
    do:
      - set_flag: tip_read
      - issue_task: ip_tracer

  - id: trace_ip
    name: "追踪 IP"
    enabled_if:
      event: receive_tip        # 单依赖可省略 all/any
    on:
      - task_issued: ip_tracer
    do:
      - add_money: { money: 500, item: usb_stick }
```

为了使下面的写法甚至更复杂的嵌套能正常工作，需要在 DAG 里加入 all 和 not 节点（目前 event 节点对入边的表现默认是 any），Trigger 添加 any、or、not 的包含其他 trigger 的逻辑 trigger
```yaml
enabled_if:
  any:                          # OR
    - all:                      # AND
        - event: task_a
        - event: task_b
    - flag: cheat_mode
    - not:                      # NOT
        event: task_c
```

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- godot-wry 无法提供可靠的页面加载状态码，因此自定义 404 只能在 ProxyOS 层提前模拟文件索引。
- 多 mod 共同提供同一域名会让路径解析、overlay、404 fallback、历史记录之间的关系变复杂，不确定当前 basic browser / basic webview / web browser app 的职责边界是否已经是最佳的。
- mod meta、mod list、pylock.toml、依赖安装与版本回滚之间还需要形成稳定流程，否则后续 mod 管理会变成新的技术债。
- AI coding 工具链仍然不可控：Claude Code 最适合但账号不稳定，Codex 的表现离谱地差肯定有什么地方出了问题，GLM 延迟过高而且 tps 也很低。

# 下期计划

- [ ] 支线任务支持
  - [ ] 剧本系统支持
- [ ] 迁移现有内容中适合 mod 化的部分（基本是完整第二章）
- [ ] 将第三章开头补充进 demo
  - [ ] 调整第二章末尾文本，引入经济系统和支线任务系统
  - [ ] 通过经济系统获得通用搭载平台
  - [ ] 将 demo 结束提示放在通用搭载平台的 app 里
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