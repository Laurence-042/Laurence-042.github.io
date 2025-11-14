+++
date = '2025-11-13T10:10:00+08:00'
draft = true
title = 'Proxyos Weekly 006'
slug = 'proxyos-weekly-006'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 能正常进第一章了，而且脚本框架已经完成，除了一些样式问题之外已经能支持第一章的完整游玩了

## 本期目标

- [ ] 修好Terminal输入光标歪的问题
  
- [x] 修好OSWindow点击时不会移动到最前方的问题
- [ ] 搞定第一章的主要游玩内容
- [ ] 看情况进行可玩性打磨

## 进展速记（Changelog）

### 新增：
  - 
### 变更：
  - 我受够在游戏里集成真实Terminal的幺蛾子了，我要搞虚拟Terminal了
### 修复：
- OSWindow点击时不会移动到最前方
- 演出脚本有命令输入回显

## 主要进展内容

之前怎么修都没修好OSWindow点击时不会移动到最前方的问题，主要是思路错了。我之前一直以DOM的那种“捕获从外向里的事件，处理后继续往里传递”的风格写程序，但是GDScript只有从里向外冒泡的阶段，这就导致我怎么打补丁都打不对。

真正靠谱的方案是在WindowManager里在_input时遍历所有窗口，确定点击的是哪个窗口，然后根据这个信息来改变OSWindow的层级，而非让OSWindow自己去处理

TODO

## 瓶颈与问题清单

- 

## 下期计划（Next）

- [ ] 

## 试玩版

暂未达到第一个试玩版的发布标准