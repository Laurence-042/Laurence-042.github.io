+++
date = '2026-09-11T09:49:00+08:00'
draft = false
title = 'Proxyos Weekly 094'
slug = 'proxyos-weekly-094'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 地图系统仍未完成，本期着重优化了剧本系统的delay特性

{{< toc >}}

# 本期目标

- [ ] 将第三章开头补充进 demo
  - [ ] 通用搭载平台的 app 
  - [ ] 将 demo 结束提示放在通过通用搭载平台回家后的场景
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

这期的核心是完成地图系统。但考虑到我上期没能找到多少codex犯的错，而它必定在奇怪的地方犯错，可以预计这期会很痛苦地给它擦屁股。

**结果：**

codex的锅
- 参数类型写错
- 漏abstract方法
- 把叙事上是后台日志的玩意写到了html文件里

没来得及完成地图系统


## 本期确定性变化

### 新增：

- 

### 变更：

- 重做delay系统，剧本系统能力扩展，使其正式支持后处理编译
- 调整了引入章的一些信息段解锁时机，使其更加自然
- 优化轻聊的界面布局，提高易用性
- 优化下载处理，添加了下载提示

### 修复：

- 修复浏览器书签无法区分多个query的bug
- 之前某次变更漏了同步翻译文件，导致key漂移后内容没对应调整，进而留下了重复条目

### 删除：

- 

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## 重构剧本系统……又一次

在上期因为引入第三章、修改第二章结尾的剧本后，这期验证时出现了运行问题——新的事件action列表变了，导致存档里之前记得action index对不上了

究其根因，是之前我们存档时以event为粒度（记录已经执行完成的event_id），但允许event执行一半直接因为delay action挂起（比如等到下个游戏日再执行后续action），产生了更细粒度的存档要求，而在这个粒度上没有可靠的追踪手段只能用action_index，而action_index无法承受action列表变更

当前我们的架构是mod侧上报story声明，然后godot侧将其解析为事件dag

因此改为使用如下方式在保留易用性的前提下彻底解决这个架构问题，然后重开新档。反正开发阶段不用考虑存档兼容：
- SendChatMessageAction之类的包含delay的action移除delay属性，改为使用delay action+send action，彻底把delay独立出来
- yaml delay action在yaml需要显式提供一个事件内唯一的restore_id，godot解析时会使用如下逻辑进行编译：
  - 解析yaml event0为godot event0
  - 解析yaml event里的action，遇到yaml delay action，将其解析为godot delay action时，godot delay action的功能是在TimeOffsetConfig指定的游戏或者现实事件设置一个变量，变量名用 __<event_id>_<restore_id>
  - 生成一个id为 __<event_id>_<restore_id>、condition为 由__<event_id>_<restore_id>变量触发的event1，把delay后面的解析出来的godot action都写到这个新event里。如果又遇到了另一个delay，同理生成event2。需要注意，解析时总会给调用的函数传入yaml event0的id，这样当yaml event里有多个delay、创建多个godot event时，其id和condition里使用的<event_id>都是yaml event0的id
- 这个机制应该为未来扩展规则做准备，所以应该实现为“支持多种解析规则，但是目前只有一个delay的规则”。这样之后加新的解析规则时，只需要加新的处理器并把它们和delay合理排序即可


移除 send_message 的 delay 后，SimpleChat 的 pending 消息队列直接使用delay的通用能力，其"延迟打断"也从 send_message 专属还原为通用能力。

## 下载处理

这个采用了注入js然后让js构建toast的方案

因为wry总是把webview渲染为子窗口，而父窗口（godot的浏览器窗口）并不能覆盖子窗口的内容，而且目前来看wry是最可靠的方案，所以只好workaround了

不过我想这个应该也没那么workaround，我毕竟看一些tauri插件本质上也是在搞这一出

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- mod meta、mod list、pylock.toml、依赖安装与版本回滚之间还需要形成稳定流程，否则后续 mod 管理会变成新的技术债。

# 下期计划

- [ ] 将第三章开头补充进 demo
  - [ ] 通用搭载平台的 app 
  - [ ] 将 demo 结束提示放在通过通用搭载平台回家后的场景
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