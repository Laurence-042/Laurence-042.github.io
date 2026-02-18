+++
date = '2026-02-16T11:22:00+08:00'
draft = false
title = 'Proxyos Weekly 033'
slug = 'proxyos-weekly-033'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 新年快乐~本期在测试中发现了早期一些遗留问题，并发现NativeWindow比预计麻烦，所以进度有些落后

{{< toc >}}

# 本期目标

- [x] 修好数据段的提示悬浮窗
- [ ] 测试第二章，并修复涉及开发环境准备和前两个任务的问题
- [ ] 优化开发环境准备和前两个任务的文案

# 进展速记（Changelog）

## 本期假设 / 预期

> 我当时以为世界是怎样的？
> 这个预期中，哪一条被证伪 / 被削弱 / 被确认？

这期有点悬，主要是Godot的子窗口支持看接口好像没有经过很好的设计，我怀疑可能存在潜在的奇异特性，而就是这个奇异特性导致的提示悬浮窗无法正常显示。

---

窗口系统重做了，连带着应用数据一起。

而且因为过年，效率低了点……

## 本期确定性变化

> 哪些东西现在「更确定」或「被明确否定」了？
> “确认 X 不可行”
> “删掉 Y 抽象”
> “意识到 Z 是伪问题”

### 新增：

- 

### 变更：

- 重做NativeWindow
- 调整SimpleChat数据模型

### 修复：

- 数据段拖动的DropArea反而不接受drop
- 点击数据段时会因弹出toolTip丢失焦点无法触发拖动，改成必须release才能弹出toolTip
- 因为获取鼠标坐标用的是对应屏幕坐标，而获取屏幕大小来对应坐标时用的是主屏幕的，导致了popup偏移
- Spider和SimpleChat存档全都不起效
- 解决累积的警告
- 一些样式问题
- Spider等content层级很高的应用会导致缩放失效

### 删除：

- 之前遗留的Desktop阶段的冗余代码

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## 重做NativeWindow

Godot 的 `DisplayServer` 只提供了 `set_icon(image: Image)` 方法，它**仅作用于主窗口**（window_id = 0），不接受 window_id 参数。对于通过 `Window` 节点创建的子窗口，**没有内置 API** 可以设置标题栏图标。

但思考了不再使用子窗口、只使用主窗口的fallback后，感觉不行——往中间调试客户端的中间塞一个浏览器界面那可太UX灾难了。

所以我使用了这么个方案：使用无边框无标题窗口打开独立窗口，然后自己做个title来支持icon和title设置，并通过信号控制最小化、最大化、关闭、拖动

1. **拖动** — `DisplayServer.window_start_drag(window_id)` 原生拖动，Windows 上甚至支持 Aero Snap 贴边
2. **调整大小** — `DisplayServer.window_start_resize(edge, window_id)` 原生缩放，不用自己算
3. **最小化/最大化** — `window.mode = Window.MODE_MINIMIZED / MODE_MAXIMIZED / MODE_WINDOWED`
4. **关闭** — 直接 `window.queue_free()`

通过这种方式，不仅能获得更高的可自定义度，之后Godot改接口了我也只用改这一个模块，维护也更加方便

## 应用数据大改

实际施工后才发现，大部分应用都需要在启动前就能处理相关数据（比如在不开浏览器的时候给浏览器加书签），之前的Saveable-AppBase-App的模式十分受限。所以改成了mvc模式，manager作为全局节点加载，然后使用存档工具类来处理存档

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

# 下下期计划

- [ ] 测试第二章，并修复涉及开发环境准备和前两个任务的问题
- [ ] 优化开发环境准备和前两个任务的文案

# 试玩版

预计第一个可玩版本将在第二章的主线内容完成后推出