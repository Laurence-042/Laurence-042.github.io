+++
date = '2025-11-13T10:10:00+08:00'
draft = false
title = 'Proxyos Weekly 006'
slug = 'proxyos-weekly-006'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> Fuck Terminal

## 本期目标

- [ ] 修好Terminal输入光标歪的问题
  
- [x] 修好OSWindow点击时不会移动到最前方的问题
- [ ] 搞定第一章的主要游玩内容
- [ ] 看情况进行可玩性打磨

## 进展速记（Changelog）

### 新增：
  - 无
### 变更：
  - 我受够在游戏里集成真实Terminal的幺蛾子了，我要搞虚拟Terminal了
### 修复：
- OSWindow点击时不会移动到最前方
- 演出脚本有命令输入回显

## 主要进展内容

之前怎么修都没修好OSWindow点击时不会移动到最前方的问题，主要是思路错了。我之前一直以DOM的那种“捕获从外向里的事件，处理后继续往里传递”的风格写程序，但是GDScript只有从里向外冒泡的阶段，这就导致我怎么打补丁都打不对。

真正靠谱的方案是在WindowManager里在_input时遍历所有窗口，确定点击的是哪个窗口，然后根据这个信息来改变OSWindow的层级，而非让OSWindow自己去处理

然后……没了

这个Terminal切成自己的之后，问题依旧一大堆，主要原因是

- GDScript不像python那样有良好的utf8支持，需要手动处理各种字符问题
- 命令执行需要新的映射方式，且需要调整Terminal的模块架构以适应当前展示、执行、命令翻译分离的状态
- 当前样式不满意，十分不Terminal，我在考虑再检查下市面上的，看看有没有可以参考的实现。
  - 或者我干脆直接用[Xterm.js](http://xtermjs.org/)？但这样外部进程通信又是个麻烦……我再看看吧

## 瓶颈与问题清单

- Terminal实现受阻，但真实Terminal确实是不可行的。因为我解决不了它间歇性好使间歇性不好使的问题。
  - 或者也许我能解决？但我需要先试试自建Terminal，实在不行再去折腾其他人代码仓


## 下期计划（Next）

- [ ] 实现靠谱的Terminal

## 试玩版

暂未达到第一个试玩版的发布标准