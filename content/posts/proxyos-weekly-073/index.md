+++
date = '2026-07-03T14:24:00+08:00'
draft = false
title = 'Proxyos Weekly 073'
slug = 'proxyos-weekly-073'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 剧本系统已完成mod化支持，迁移已部分完成（主要是网页部分）但仍有缺陷需要处理

{{< toc >}}

# 本期目标

- [x] 支线任务支持
  - [x] 剧本系统支持
- [ ] 迁移现有内容中适合 mod 化的部分（基本是完整第二章）
  - [x] 网页前端
  - [x] 网页后端
  - [ ] 任务、剧本、桌宠等资源
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

……我考虑下期休息一期，这期的第一天就遭遇了愣是睡不着导致直接通宵、第二天也是 2 点才睡着的灾难，以至于这个半周报都是下午才创建

这期我准备聚焦于现有内容的迁移与第三章开头的设计与实现，降低代码部分的工作量，避免神志不清导致和 codex 一起往项目里拉屎

**结果：**

说实话有点虚……改得比我想象得多，虽然暂时看搞定了，但我高度怀疑我给未来的自己埋了坑

## 本期确定性变化

### 新增：

- 实现了剧本系统的 mod 化
- 补齐了 mod 侧的全 EventAction 能力

### 变更：

- 调整了主场景加载逻辑，使其流程更加清晰，也更符合 mod 架构
- 调整了剧本系统的挂载逻辑，并让其命名更加清晰
- 将 json store 能力作为 EventAction 提供，而不是作为专用 method
- 优化了 json 实现
- 将第二

### 修复：

- 修复了 codex 犯的一系列诸如变量名用保留字、对 Variant 返回值用自动类型推断、多个同义参数走不同处理流程的各种傻逼问题
- 修复 proxy_os_ipc 分包导致的 server 找不到 player 包定义的问题，以及一些类型标注问题

### 删除：

- 

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## 关于 Mod

因为篇幅较长，我将其单独拆出来写了个 [Proxyos Mod 系统介绍](../proxyos-mod)

## 关于剧本系统

相较于上期的粗略设计，简化了书写，让各个命名更明确，并区分了依赖其他事件的`after`和决定`on`是否可以触发的`enable_if`

其实际上扩充了原本剧本系统的能力，为剧本系统提供了更复杂的控制

```yaml
meta:
  id: branch_demo
  name: 分支示例

events:
  - id: issue_entry
    name: 阶段开始时签发任务
    on:
      stage_entered: 2
    do:
      - activate_and_issue_task: "[my_mod]_[author]_entry"

  - id: remember_choice
    name: 完成任务后记录选择
    after: issue_entry
    on:
      task_completed: "[my_mod]_[author]_entry"
    do:
      - set_var:
          key: route.choice
          value: "left"
      - set_flag: entry_done

  - id: left_branch
    name: 左分支任务
    after: remember_choice
    enable_if:
      var_eq:
        key: route.choice
        value: "left"
    on:
      flag: entry_done
    do:
      - activate_and_issue_task: "[my_mod]_[author]_left_branch"
```

其甚至可以自定义 enable_if、on 的 handler：

```python
from proxy_os_ipc.sdk.story import action_handler, condition_handler
from proxy_os_ipc.sdk.notification import NotificationType, notification

@condition_handler("[my_mod]_[author]_has_signal")
async def has_signal(args: dict) -> bool:
    return args.get("signal") == "ECHO-042"

@action_handler("[my_mod]_[author]_notify_signal")
async def notify_signal(args: dict) -> None:
    await notification.show(
        "Echo Trace",
        str(args.get("message", "信号已确认。")),
        notification_type=NotificationType.INFO,
        notification_id="echo_trace_signal_confirmed",
    )
```

```yaml
meta:
  id: custom_demo
events:
  - id: custom_gate
    on:
      custom:
        handler: "[my_mod]_[author]_has_signal"
        args:
          signal: "ECHO-042"
    do:
      - custom:
          handler: "[my_mod]_[author]_notify_signal"
          args:
            message: "收到 ECHO-042。"
```

如果您之前一致跟进这个项目，可能会注意到之前的“Trigger-Action”变成“Condition-Action”了，这是有意为之的。

因为要想避免 `on`和`enable_if` 分别实现any、all、not，那它俩就得使用完全相同的处理方式。这种情况下Trigger这个名字虽然还适合前者但不适合后者了，因此进行了更名与能力扩充

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- godot-wry 无法提供可靠的页面加载状态码，因此自定义 404 只能在 ProxyOS 层提前模拟文件索引。
  - 这个我想确实只能这样了。我也想了其他方法，比如扩展route_table能力、让python侧可以自行决定route等等，但不是在三方项目里拉屎就是凭空加复杂度
- 多 mod 共同提供同一域名会让路径解析、overlay、404 fallback、历史记录之间的关系变复杂，不确定当前 basic browser / basic webview / web browser app 的职责边界是否已经是最佳的。
- mod meta、mod list、pylock.toml、依赖安装与版本回滚之间还需要形成稳定流程，否则后续 mod 管理会变成新的技术债。
- AI coding 工具链仍然不可控：Claude Code 最适合但账号不稳定，Codex 的表现离谱地差肯定有什么地方出了问题，GLM 延迟过高而且 tps 也很低。
  - Codex只要一直使用plan模式，其表现总体可控，勉强可用

# 下下期计划

- [ ] 迁移现有内容中适合 mod 化的部分（基本是完整第二章）
  - [ ] 任务、剧本、桌宠等资源
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