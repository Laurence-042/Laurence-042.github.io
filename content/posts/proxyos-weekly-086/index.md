+++
date = '2026-08-14T12:56:00+08:00'
draft = false
title = 'Proxyos Weekly 086'
slug = 'proxyos-weekly-086'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 主要修复了复杂网页上才会暴露出的一些问题
>
> 作息乱了，下期可能歇一期

{{< toc >}}

# 本期目标

- [ ] 完整冒烟
  - [ ] 第 2 章
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

冒烟通跑

**结果：**

还是没跑完……

问题远比预想的多

## 本期确定性变化

### 新增：

- 

### 变更：

- 稳定化伪 http 架构的各种约定
- 优化第二章引导任务的流程，使其更符合 lore 且更符合玩家直觉
- 优化了网站上的一些明显翻译问题
- 把被 codex 写成屎的控制面板界面结构重新梳理并重构为职责清晰可维护的模式
- 优化时间显示，并抽取为单独控件，godot 侧可以使用统一的时间控件了
- 允许复制通知内容

### 修复：

- 修复应用窗口最小化后从任务栏消失、通过再次打开应用窗口恢复时显示出现异常的 bug
- 彻底修复翻译产物 overlay 中的字面`\n`及其根因导致的网页结构异常（本质上是在不该 strip 的地方 strip，在不该转义的地方转义了）
- 修复 404 页面导航在路由表大修后失效的 bug
- 修复茶馆的注册和登录在伪 http 架构大修后失效的 bug
- 修复玄云观的一个链接因为翻译结果网站和逗号连在一起，导致逗号成为网址一部分的 bug
- 修复玄云观的网页框架设计问题导致的页面 404 和漏翻译

### 删除：

- 

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## 应用窗口最小化后从任务栏消失、通过再次打开应用窗口恢复时显示出现异常的 bug

这个属实有点微妙，因为我用的是 Godot 提供的原生窗口和原生窗口最小化 API，但是还是出问题

经过检查后，问题根因倒是清楚了：Godot 引擎自己的问题，Godot 4.6.2 在 `SW_MINIMIZE` 之后重建 HWND style 时，把 `WS_VISIBLE` 去掉了。

### 问题路径

Godot 4.6.2 的 `window_set_mode()`：

```cpp
if (p_mode == WINDOW_MODE_MINIMIZED) {
    ShowWindow(wd.hWnd, SW_MINIMIZE);
    wd.maximized = false;
    wd.minimized = true;
    wd.was_fullscreen_pre_min = was_fullscreen;
}

...

_update_window_style(p_window, false);
```

也就是说顺序就是：

** `SW_MINIMIZE` → 设置 `wd.minimized = true` → 重建整个 Windows style。**

而 `_get_window_style()`：

```cpp
if (p_main_window) {
    ...
    if (p_initialized) {
        r_style |= WS_VISIBLE;
    }
}

...

if (!p_borderless && !p_no_activate_focus && p_initialized) {
    r_style |= WS_VISIBLE;
}
```

所以对于我那个 非主窗口 + borderless + initialized + 非 no-focus 的场景

最终 `_get_window_style()` 返回的 `style` **没有 `WS_VISIBLE`**。

然后 `_update_window_style()` 又

```cpp
SetWindowLongPtr(wd.hWnd, GWL_STYLE, style);
```

用这个覆盖了原来的 style，导致任务栏按钮消失。

而那个从新打开后显示异常的问题大概率也是类似路径。

### 解决方法

这个我没给 godot 提 pr，因为这个属实有点系统底层了，我也不十分清楚 windows 窗口的所有行为，贸然变更可能引出更多其他非预期行为。

不过之前发现 godot 没提供设置原生 window 图标的能力时，因为觉得为了这个去深入了解 godot 架构并提 pr 感觉不太值当，所以干脆自己搓了个 python 进程用 ipc 设置图标。这次也是类似场景，所以我干脆把它扩展了下，同时也让它负责窗口最小化，绕过 Godot 的流程。

我确实讨厌头痛医头脚痛医脚的 patch 式修复行为，不过我更讨厌为了自己的一点小问题改坏大项目的拉屎行为，所以该 patch 还是得 patch 的

## 伪 http

### 缺失的历史

最开始，我是为了让 godot 能调 python 脚本、python 脚本运行中上报数据才做了 ipc（实际上最开始用的是 stdout，但后来发现这玩意的 flush 十分难以控制，而且只有一个信道难以扩展，然后才开始用 websocket 做 ipc）

然后有了 web 侧后，我也自然地想都没想就把 godot 和 web 侧的交互也绑上这个 ipc 了，甚至在 mod 化重构的时候都直接把作为网页后端服务的 python 脚本也用这个 ipc 注册自定义 route 了

但现在仔细想想，我好像没有很认真想过要不要让 python 侧用 http

诚然，我在 [第 26 期](../proxyos-weekly-026.md) 曾经说过

> ……感觉不如直接就借此机会把之后章节需要的 rest 接口编程的基础设施搞定，所以我第一时间想要不要干脆引入完整 HTTP。 
> 但是进行了技术调研后发现，Godot 并不自带 http 支持，而且即使支持，我也得在 python 里整一套 proxy://到 http://的转换模块。 
> 于是我决定干脆用 Socket，简单、跨平台、可以完全控制消息结构与映射关系，而且没有复杂的解析性能也会更好。

但是当时更多的是在实现代价上分析的，而不是真的从功能上分析。

### 优势

- curl 调试和标准工具链——开发体验上是真提升
- 中间件生态（鉴权、校验）和 OpenAPI 文档会更方便
- 不用自己维护那 50 行协议
- 所有 http 特性支持，可以让 mod 作者给玩家做靶场玩

### 劣势

- 目前大量使用 python 和 godot 的双向调用，即使 python 侧完全 http，godot 侧仍然需要 websocket 来接 python 侧的主动调用（毕竟 gdscript 没有 http server）
- 真实 http 的约束也更强，没法搞太离谱的狠活
- 真实 http 的端口和路由机制可能会带来更多的适配问题
- 可能不符合游戏 lore，毕竟设定上其实用的不是 http 而是 proxy

### 分析
双向调用是基础，单单 http 满足不了这个基础

切成 http 后收益暂时不明显

### 结论

暂时继续 IPC，如果以后真的做大了需要真 http，再改用 [ASGI](https://asgi.readthedocs.io/en/latest/introduction.html) 来兼容 WebSocket 和 http

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- mod meta、mod list、pylock.toml、依赖安装与版本回滚之间还需要形成稳定流程，否则后续 mod 管理会变成新的技术债。

# 下期计划

- [ ] 完整冒烟
  - [ ] 第 2 章
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