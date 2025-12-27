+++
date = '2025-12-27T10:52:00+08:00'
draft = false
title = 'Proxyos Weekly 018'
slug = 'proxyos-weekly-018'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 正式接入了ANORA，完成了第一章的所有机制，同时完成了其内容草稿。

{{< toc >}}

# 本期目标

- [x] 适配相关关卡脚本
  - [x] python脚本输出特定指令控制GDScript控制逻辑图

# 进展速记（Changelog）

## 本期假设 / 预期
> 我当时以为世界是怎样的？
> 这个预期中，哪一条被证伪 / 被削弱 / 被确认？

- 我应该可以通过ANORA上预留的IPC和godot-wry的IPC机制对接
  - 实际上其遇到了单页面应用不兼容、IPC协议不兼容的问题需要解决
- 脚本机制已经完善了，只需要填内容
  - 实际上交互机制实际试玩了才会发现根本一坨，于是重构了

## 本期确定性变化
> 哪些东西现在「更确定」或「被明确否定」了？
> “确认 X 不可行”
> “删掉 Y 抽象”
> “意识到 Z 是伪问题”

### 新增：

### 变更：

- 优化1-3关关卡脚本，尝试加强剧情张力
- 调整IPC传输的数据模型，使其更加符合一般习惯

### 修复：

- 脚本完成后因为midware不对导致任务没有正常完成
- ANORA的IPC初始化始终未执行
- ANORA的IPC不兼容godot-wry

### 删除：


# 主要进展内容/本期关键判断点
> 我做出了哪些「如果错了也要付代价」的判断？

## 调整第一章的Typewriter模式

先前使用如下输出循环
- 逐字输出一句话
- 指定延迟多久后继续执行

而这个方案存在明显问题：有时候同一个角色的一次发言需要分多行，这种情况下多行之间是不应该有延迟的

于是我尝试了使用一个状态机来维护什么时候有延迟、什么时候忽略。并将默认延迟根据平均阅读速度按字数计算，以自适应延迟

但发现它仍有问题：读得快的人只能硬等，读得慢的人还是跟不上

于是现在切成了类似galgame的逻辑：一段发言之内的多句话不再有延迟，用户按Enter键后才会显示下一段发言

## ANORA的正式对接

先前很自然地以为自己搞定了两边
- ANORA纯前端
- 在ANORA里实现了符合浏览器IPC标准的`window.addEvenListener`
- Godot有godot-wry可以展示本地网页

于是我就误以为对接是水到渠成的事，但实际上情况是
- 浏览器：按照标准方案，进程间、页面间通信应该用window.sendMessage和window.addEventListener('message'实现
- tauri：标准方案太挫了，很容易被干扰，而且信息也太杂。我给它诸如个私有的进程间通信桥梁
- godot-wry：tauri的wry不错，可以拿来开发godot的浏览器支持。但是tauri的方案太复杂了，window.sendMessage的信道也太杂了还容易被网站的奇奇怪怪配置搞出问题，我就用document.dispatchEvent吧
- 我：按照标准方案开发了兼容，然后发现接不上godot-wry

而且ANORA是使用vue router的单页面应用，其默认的clean url（不使用hash区分单页面内部route的）被现代浏览器支持，但是godot-wry自定义的兼容Godot的res协议实际上是纯文件访问，clean url能定位到anora/index.html和anora/这种根页面文件，但不能定位到anora/demo这种内部route。

实际情况甚至更麻烦，因为vue route是使用url判断自己当前应该加载单页面中的哪个vue的，但是godot-wry会使访问anora/时路径变为anora/index.html，这就使其route没有识别到当前在根路由`/`对应的view，结果就是main.ts里的东西执行了，但是view完全没加载只有个空的`<div id='app'>`

所以结果自然就是ANORA的route从`createWebHistory`切成了`createWebHashHistory`——你总不能指望我去给godot-wry整个完整的单页面应用支持，单单把它的`load_url`修成支持res协议的已经是我的接受上限了。然后ANORA的IPC也做了window和document的兼容，毕竟godot-wry在其预设场景中，使用document的自定义事件确实是最有性价比的方案

# 瓶颈与问题清单
> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- 同时有Terminal和对照用的ANOWRA的界面交互仍需优化，当前上下分屏也许不是最优方案

# 下期计划（Next）

- [ ] 细化第一章剧本，使其足以确认我需要实现哪些机制
- [ ] 思考当前界面如何进行优化

# 试玩版

预计第一个可玩版本将在第二章的第一个涉及外部编程的游戏内容完成后推出