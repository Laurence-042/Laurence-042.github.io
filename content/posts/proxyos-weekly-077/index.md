+++
date = '2026-07-16T14:13:00+08:00'
draft = false
title = 'Proxyos Weekly 077'
slug = 'proxyos-weekly-077'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 

{{< toc >}}

# 本期目标

- [ ] 修 bug
  - [x] mod 数据加载
    - [x] 常规数据扫描
    - [ ] overlay合并
    - [ ] 网页 route
  - [ ] 基于 SpiderView 的 mod 自定义 AppView 冒烟
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

这期的核心是完成主流程冒烟，即直接玩完第一章

这个游戏的教程章实际上包含了几乎所有机制，剩下的都只是对这些机制的灵活应用罢了

**结果：**

问题忒多，最终时间都花在了翻译工具修复和收拾codex的烂摊子上



## 本期确定性变化

### 新增：

- 翻译工具可以显式忽略某个目录
- 两个支线任务的设计

### 变更：

- 优化Mod侧任务定义数据结构，与内部实现解耦
- 优化story yaml加载架构
- 优化等待翻译设置应用完成的逻辑，现在其更加可扩展了，也可以等待godot内的异步设置应用了
- 将CopyFile从同步IO改为异步IO
- 优化翻译工具的报错信息，使其足够支持错误定位
- 优化浏览器架构，使其更易维护，数据流更清晰，并允许自定义后端handler覆盖某些url的网页

### 修复：

- 修正codex搞出来的保留字变量名、类型推断结果是Variant之类的幺蛾子
- 修正codex搞出来的悬空函数引用
- 修复story无法在切换语言时正常重新合并overlay的bug
- 修正codex没搞好的数据加载
- 修正codex没搞好的@tool标记和非async函数被await警告
- 修复翻译工具对godot侧的翻译遗漏
- 将莫名其妙变成UTF-8-sig的文件改回UTF-8

### 删除：

- 过时的翻译

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## 追查奇怪的悬空引用

在继承测试时，发现了不能存在的 _apply_cached_mod_chapter_event_payload 的调用。然后开始追查其来源。

### 流程调查

从git记录来看，案发流程是：

- **2026-07-09 14:39:12**，提交 `b4ca6a685c4994f40499d748e8368e390fb41d79` 首次加入：

  - `_mod_chapter_event_configs`
  - `_apply_cached_mod_chapter_event_payload()`
  - `setup_for_control_panel()` 中的补应用调用

- **约 7 小时后**，提交 `7657320e7e783a87825b05e817a0f9b6f4a892e9` 在引入 `StoryYamlCompiler`、把故事配置切换为 YAML 编译时：

  - 删除了 `_mod_chapter_event_configs`

  - 删除了 `_apply_cached_mod_chapter_event_payload()`

  - 将 `_on_framework_ready_story()` 改成收到 payload 后直接调用：

    ```
    data_controller.apply_mod_chapter_event_payload(payload.chapter_event_configs)
    ```

  - 但漏删了 `setup_for_control_panel()` 里的：

    ```
    _apply_cached_mod_chapter_event_payload()
    ```

所以确实是在Story yaml化时，删除历史逻辑时没有做好收尾。

### 背景推测

从代码记录和我即将消逝的模糊记忆来看，应该是
第一版实现里：

- 在Python侧把yaml编译成了godot里的格式
- 以json serialization传到了godot侧直接使用
- godot侧的ChapterControllerManager缓存传递的Story，传递给当前的ChapterController
- 当ChapterController被重新创建时，ChapterControllerManager将缓存的Mod侧Story传入新的ChapterController

随后因为

- Python侧不该了解Godot侧实际数据格式
- Godot侧没必要缓存，直接写入即可

进而改成了：

- 在Python侧把yaml直接传到godot侧
- godot侧解析后写入ChapterController

### 流程复查

可以注意到，这里隐式依赖了时序。如果framework_ready时ChapterController未加载，那就可能丢数据，而且ChapterController重新创建时也无法再次写入

但这应该不是问题，因为目前加载时序由godot侧entry控制，具体流程如下

1. `main.gd` 实例化 `ControlPanel`
2. `add_child(level)` 触发 `ControlPanel._ready()`
3. `ControlPanel._ready()` 调用 `ChapterControllerManagerNode.setup_for_control_panel(self)`，controller 已创建
4. `main.gd` 用 `call_deferred()` 启动 `_run_control_panel_boot_loading()`
5. 它再调用 `FrameworkLauncherNode.start_and_wait_ready()`
6. framework 收到数据后同步 `dispatch_event("framework_ready.story", ...)`
7. manager 此时可以直接把 payload 应用到已经存在的 controller
8. `start_and_wait_ready()` 返回后，`main.gd` mount chapter events，再扫描任务

而且ChapterController一般也不会在程序的生命周期内重新创建

## 数据传递架构调整

我遇到一个架构问题。当前项目因为json很多，所以翻译模式使用了overlay。而且当前项目的所有内容几乎都是mod实现。所以其启动逻辑是
- 主程序启动mod loader
- loader判断mod顺序，按照mod顺序依次要求各个component去加载对应mod里自己负责的资源和资源overlay
- loader汇总这些资源，传递给主程序
- 主程序根据loader传来的资源内容、资源文件名、资源overlay，将其中相对资源文件的路径解析为相对项目的路径，并进行overlay合并。之后引用资源文件里的路径时自行把路径做overlay找对应并与base合并

也就是说，目前路径解析在主程序侧，这当时是考虑到切换语言时可以让主程序直接将引用/path/_overlay/lang0的映射为引用/path/_overlay/lang1，而不必让component重新报对应语言的数据。

主程序和component两侧使用不同的语言实现，通过ipc交互，ipc消息类型越少越好。

但现在这个项目要加个翻译流水线，component在发现资源时还需要上报资源的位置和需要翻译的字段。这就导致其也需要解析路径引用来找引用文件，进而导致了两套路径解析。

- 如果只在 component 侧做解析路径，那么切换语言后目标overlay的路径就变了，需要component侧重新解析
- 使用逻辑id的方案也不合适，因为其会导致配置复杂，给维护者带来额外负担

而这个矛盾是因为我把“将路径规范化到相对于mod_root”和“解释规范路径的overlay路径（json和yaml合并base和overlay、其他文件直接使用overlay）”绑定了，而实际上它们是两个步骤

我想正确的架构应该是mod侧做路径规范化。这样component做翻译上报的时候就能直接给i18n发标准的、相对mod_root的路径并快速claim。上报到godot侧后godot侧也不用管文件的相对路径，直接统一当规范的、相对mod_root路径用，并在使用路径时根据业务决定是merge还是使用overlay即可

## 浏览器框架调整

这次算是真正敲定框架了。详情可以参考

[Proxyos 浏览器系统介绍](./proxyos-spider)

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- mod meta、mod list、pylock.toml、依赖安装与版本回滚之间还需要形成稳定流程，否则后续 mod 管理会变成新的技术债。
  

# 下期计划

- [ ] 

# 试玩版

暂缓，第一次上传需要做好准备，等进入 beta 阶段再说