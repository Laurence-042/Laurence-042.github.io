+++
date = '2026-03-10T11:22:00+08:00'
draft = false
title = 'Proxyos Weekly 040'
slug = 'proxyos-weekly-040'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 界面问题差不多完事了，下期优化内容

{{< toc >}}

# 本期目标

- [ ] 一个打磨完的 demo
  - [x] 把界面框架打磨完，内容可以下下期

# 进展速记（Changelog）

## 本期假设 / 预期

> 我当时以为世界是怎样的？
> 这个预期中，哪一条被证伪 / 被削弱 / 被确认？

这一期会主要对界面进行优化，文案问题不大，但可能有些文案的表达方式需要改

---

确实如此，优化了很多界面。不过文案部分还没有深入检查，也许仍存在问题

## 本期确定性变化

> 哪些东西现在「更确定」或「被明确否定」了？
> “确认 X 不可行”
> “删掉 Y 抽象”
> “意识到 Z 是伪问题”

### 新增：

- 添加了设置界面
- 添加了根据 DPI 自动缩放文字的特性，现在在高 DPI 屏幕上不会字体过小了

### 变更：

- 优化了启动流程，避免玩家在初始化过程中进行操作导致出现不可预期的错误
- 优化界面，使其更加符合认知习惯，也更正了一些不恰当的表达
- 重构应用启动侧边栏的布局、图标及加载机制，现在它们表现更加一致了，而且之后要扩展也会更方便，甚至可以支持 mod

### 修复：

- 为确认退出的对话框添加了缺失的取消选项
- 解决窗口最大化后无法正常操作且任务栏不再显示图标的问题
- 解决窗口系统的多显示器适配问题

### 删除：

- 彻底退役显示在游戏主窗口内部的旧窗口系统

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

没啥可说的，基本就是在修 bug、改界面

唯一值得一提的就是窗口系统的“Ghost”鬼影问题

## 问题现象

游戏内自定义无边框窗口点击还原（从假最大化恢复到原尺寸）后，屏幕上残留一块与最大化尺寸相同的透明/空白区域（Ghost），直到窗口被移动或重绘才消失。

而这个鬼影可以接受点击事件，并在还原后的窗口中呈现对应点击结果，但各个元素的视觉和实际事件判定范围却又有偏差。

## 根因排查路径

排查过程中依次发现并确认了四个独立根因，均通过日志对比 _window.size 与 DisplayServer.window_get_size() 的返回值来定位：

### wrap_controls = true（最初根因）
Godot 每帧用子节点 minimum_size 覆盖 Window.size，导致 Godot viewport 与 OS framebuffer 长期不同步，是 ghost 出现的基础条件。

### DisplayServer.window_set_size() 无法缩小窗口（方案排除）
日志显示调用后 _window.size 已变回 (600,500)，但 DisplayServer.window_get_size() 仍为 (3838,2088)——Windows 以当前 GL surface 大小作为下限，拒绝缩小。RenderingServer.force_draw() 同样无效，仅刷新 Godot 渲染层，无法触及 OS compositor。

### _window.position 是父窗口相对坐标，直接用于屏幕定位产生双重偏移
_window.position 相对 Godot 主窗口，而 screen_get_usable_rect() 和 mouse_get_position() 返回绝对屏幕坐标。混用导致多屏场景下最大化后位置偏移 2304px（第二块屏幕起始坐标叠加两次）。

### hide()+show() 后 initial_position = CENTER_MAIN_WINDOW_SCREEN 重新触发居中
该枚举值在每次 show() 时都生效，导致还原后窗口跑到屏幕中央而非原位置。同时，show() 后 OS 可能重建窗口句柄，旧 window_id 失效引发 !windows.has(p_window) 崩溃。

## 最终解决方案

唯一能强制 OS 释放旧 framebuffer 的方式是 hide() → 修改尺寸 → show()，配合以下三处修复：

| 修复位置                                              | 修改内容                                                     |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| `NativeWindowManager.open_window()`                   | `window.wrap_controls = false`                               |
| `NativeWindowManager._show_window()`                  | 第一次 `show()` 后立即切换 `initial_position = ABSOLUTE`     |
| `NativeWindowTitleBar._apply/restore_fake_maximize()` | 保存/恢复位置改用 `DisplayServer.window_get/set_position()`（绝对坐标）；`show()` 后重新调用 `get_window_id()` 取新句柄 |

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

说实话，这次的 Ghost 问题极大程度依赖了 claude。因为我确实对这种工具相关问题没辙。虽然问题已经解决了，甚至让 claude 总结了问题路径（就是上一节），但说实话我仍不觉得这是最佳方案。但总比有问题强，对吧？

# 下期计划

- [ ] 一个打磨完的 demo

# 试玩版

预计第一个可玩版本将在第二章的主线内容完成后推出