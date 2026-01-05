+++
date = '2025-11-17T14:46:00+08:00'
draft = false
title = 'Proxyos Weekly 007'
slug = 'proxyos-weekly-007'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 把Terminal的方案退回了真实Terminal，修了些第三方库的bug，然后爆改了第一章

## 本期目标

- [x] 实现靠谱的Terminal
- [x] 重构第一章游玩结构
- [ ] 完成第一章游玩内容

## 进展速记（Changelog）

### 新增：
  - 无
### 变更：
  - 回退到了真实Terminal方案
  - 将最开始的“自动进行下一个教学”改成了“玩家需要手动依次触发相关教学”
### 修复：
- 修好了GodotXterm里野指针导致的高频偶现问题

## 主要进展内容

在详细分析后，发现一旦涉及执行外部程序并实时显示stdout，那么自建Terminal的问题就会多到难以置信，而且市面上也缺乏支持良好的——这本质上就是实现正经Terminal了

所以最后还是切回了真实Terminal的方案，并借助Copilot修好了那个间歇性好使间歇性不好使的问题。问题路径是

- 在获取`cwd_` 参数时，使用了`const char* cwd_ = p_cwd.utf8().get_data();`
  - `.utf8()`创建一个临时的 UTF8 buffer（CharString）
  - `.get_data()`取出它的内部 char*
  - **临时对象被销毁**
  - `cwd_` 指向已经释放的内存 → **悬空指针**
- 随后又使用`std::string helper_path = p_helper_path.utf8().get_data();`
  - `.utf8()`再次分配到了`cwd_ `指向的内存上
- 在`CreateProcess`时引用`cwd_` 作为工作目录
  - `helper_path `是一个可执行程序，而非目录
- ConPTY进程创建失败

然而上面那个并非唯一问题，因为它没有正确处理pipe，导致同一个PTY对象只能fork一次。虽然每次instantiate也不是不行，但还是借助Copilot+Claude给修了

![](ChatGPT%20Image%202025年11月17日%2014_59_57.png)

然后就是剧本和一开始有差异。最开始的设计中，我使用“自动依次执行对应的python教学脚本”的方式。但我试玩了一下发现这样很无聊。所以加了俩自定义命令diagnose和manualfix，来分别展示目前修复进度和调用教学脚本。虽然玩家的游玩路线没有变，而且本质上是增加了麻烦，但是自己执行命令来启动脚本对于新手来说应该还是有些意思的，而且即使对于老手应该也能冲淡一个个教学脚本带来的粘滞感

再之后就是我重写了第一章的前两节，之前的剧本有点太挫了，没有很好地和游戏世界观相融合，所以我正在整个重写

## 瓶颈与问题清单

- 


## 下期计划（Next）

- [ ] 完成第一章游玩内容
  - [ ] 这个真得完成了，都TM拖3期了


## 试玩版

暂未达到第一个试玩版的发布标准