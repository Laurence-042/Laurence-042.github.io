+++
date = '2026-04-30T11:30:00+08:00'
draft = false
title = 'Proxyos Weekly 055'
slug = 'proxyos-weekly-055'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 第一章重置完成，第二章重置WIP

{{< toc >}}

# 本期目标


- [ ] 把 demo 从 alpha 打磨到 beta
  - [ ] 第一章 
    - [ ] 【低优先级】xterm 的 col 似乎计算不太对劲，有时候一行末尾的字只显示了一半，需要看下 xterm 实现，必要的话进行修复
    - [ ] 【低优先级】xterm 的 cursor_pos 在 cursor 不在视野内时返回末行 pos 是个 bug，而且在外面基本没法绕，只能修 xterm
    - [x] 完成第一章的测试和润色
    - [x] 将编程手册提前到第一章，并随第一章进度逐渐丰富内容，而不是第二章再解锁
  - [ ] 第二章
    - [ ] 调整文案以适应安全内核的角色调整
    - [ ] 将安全内核结合内部编辑器作为小黄鸭提示来避免卡关
      - [ ] 核心系统
      - [ ] 内容补充
      - [ ] 测试
  - [ ] 优化剧本系统架构，使存档系统以其为核心，每个 Event 完成后才存档，以此保证 Trigger+Actions 组成的 Event 的原子性
- [ ] beta 打磨完成后
  - [ ] 开个 itch
  - [ ] 琢磨下宣传

# 进展速记

## 本期假设 / 预期

**预期：**

第一天（4.30）趁plan quota reset 前把第二章的小黄鸭提示系统搞定，随后三天歇一天，剩下两天一天搞定第一章，一天折腾第二章文案

**结果：**

5.2额外休了半天，前三期为了好好利用Copilot付费方案变更带来的凭空1个月的quota直接没歇，这期有点累……

大部分预期内容都搞定了，只有第二章文案只搞了1/3

## 本期确定性变化

### 新增：

- 添加了第一章到第二章的过渡文案
- 第二章文案进度1/3

### 变更：

- 优化了第一章玩家和代码的交互逻辑，现在交互更加自然，纯演示性代码的表现也得到了优化
- 优化了lesson05的代码，玩家更不容易操作出错了
- 将编程手册提前到了第一章，并随玩家进展实时更新

### 修复：

- 修复template渲染时空行不显示的bug
- 修复template渲染时`[`出现了转译符号的bug
- 修复#BREAKPOINT#被没正常生效的bug
- 修复lesson01的username在保存时带上了额外的单引号的bug
- 修复单步调试无法长期运行的bug

### 删除：

- 

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## TMD 循环依赖

事情的起因是，新加的测试场景跑不起来了，一跑就会在 AppRegistry 里报 debug 的应用场景相关配置资源 debug_app_def_scene_pack.tres 加载失败

然后我和claude都在怀疑是UID有问题，但仔细检查、各种清缓存、重新生成都没有解决问题

而claude这时候还在坚持UID问题，所以就得我亲自上手了。测试工作的经验：当看到一个问题时，先尽可能缩小问题触发条件，信息越多，范围越小，越有助于找到问题根因

- 让 debug_app_def_scene_pack.tres 使用setting_app的tscn：问题消失
- 将 debug_app_def_scene_pack.tres 使用的 debug_panel 场景里的脚本引用删除（即让debug_panel.tscn里的DebugPanel不关联debug_panel.gd）：问题消失

我确认文件级最小问题根因出在 debug_panel.gd 上

但因为显示加载问题，所以我第一时间开始怀疑出现了循环依赖

claude opus 4.7 High thinking 后觉得也是这样，然后给出了一个字很多看似很有道理的理论：
```
project.godot:20：AppRegistryNode 是第一个 autoload。
app_registry.gd:16 在 _ready() 里同步扫描并 load() 整个 app_def_scene_packs/ 目录。
加载 debug_app_def_scene_pack.tres → 解析其 ext_resource → 加载 debug_panel.tscn → 加载根节点脚本 debug_panel.gd。
编译 debug_panel.gd 时需要解析它引用的所有类型/标识符（TaskManagerNode、DataSegmentManagerNode、GameProgressManager、ChapterEventConfig、TaskSaveData 等）——这要求 GDScript 加载相应的脚本。
加载 task_manager.gd:17 时，它有：
pocket_app_def.tres 也是 app_def_scene_packs/ 扫描链上的兄弟资源。
资源加载器此时检测到正在 mid-load 的资源被嵌套加载 → 返回 null → 上层 .tscn 解析器抛出 "non-existent resource" Parse Error。
```

要不是因为我真的会godot，真被他忽悠过去了。因为load是同步加载，不会出现这种前一个load影响下一个load的情况——AppRegistry的load清单都是由资源扫描模块提供的，它自己都不知道load顺序

于是我开始进一步调试，然后发现了更奇怪的现象：MainSceneLoader被加载了，而且它也在报load失败

于是我尝试从main.gd里移除control_panel_scene相关逻辑后，发现问题再次消失

所以问题就出在main、control_panel、debug_panel的关系上！

于是溜了眼，哦豁，control_panel和debug_panel都在调MainSceneLoader来改游戏进程，而MainSceneLoader是control_panel的加载者也依赖control_panel，于是就循环依赖了

但这时候claude的方案还是“把MainSceneLoader的场景依赖放到场景里配置，而不是在MainSceneLoader的脚本里写preload”，我当即质疑问题的核心是“MainSceneLoader作为场景加载者就不该被任何场景引用”

claude秒开智，意识到应该把游戏进程的操作放到autoload的全局单例GameProcessManager里，让control_panel和debug_panel调GameProcessManager修改游戏进程，而MainSceneLoader则listen GameProcess 的变更来做加载行为，这才把问题解决

不得不说，这里面哪怕只有一步被claude忽悠过去了，问题没解决不说，项目里还得多一堆屎

## 将编程手册提前到了第一章，并随玩家进展实时更新

之前的“第一章教学，第二章获得教学汇总用于在完成第二章任务时对照”的思路不合适，因为玩家可能会花费多天来完成教学，这就会导致其容易忘记。所以需要及时提供备忘

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

# 下期计划

- [ ] 把 demo 从 alpha 打磨到 beta
  - [ ] 第一章 
    - [ ] 【低优先级】xterm 的 col 似乎计算不太对劲，有时候一行末尾的字只显示了一半，需要看下 xterm 实现，必要的话进行修复
    - [ ] 【低优先级】xterm 的 cursor_pos 在 cursor 不在视野内时返回末行 pos 是个 bug，而且在外面基本没法绕，只能修 xterm
  - [ ] 第二章
    - [ ] 调整文案以适应安全内核的角色调整
    - [ ] 将安全内核结合内部编辑器作为小黄鸭提示来避免卡关
      - [ ] 核心系统
      - [ ] 内容补充
      - [ ] 测试
  - [ ] 优化剧本系统架构，使存档系统以其为核心，每个 Event 完成后才存档，以此保证 Trigger+Actions 组成的 Event 的原子性
- [ ] beta 打磨完成后
  - [ ] 开个 itch
  - [ ] 琢磨下宣传

# 试玩版

暂缓，第一次上传需要做好准备，等进入 beta 阶段再说