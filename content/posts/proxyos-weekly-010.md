+++
date = '2025-11-30T21:20:00+08:00'
draft = false
title = 'Proxyos Weekly 010'
slug = 'proxyos-weekly-010'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 问题远比预想的多，一直在调Terminal和修改架构

## 本期目标

- [ ] 完成第一章
  - [ ] 更新当前交互脚本基础框架
  - [ ] 实现六节的脚本
- [ ] 重新审视目前的章节切换流程，确保其扩展到三章时不出大问题

## 进展速记（Changelog）

### 新增：
  - 一个仍有很大问题的，在修复阶段用于辅助说明的逻辑图系统（也是为ANORA进行技术试水，其前身AAW的架构可能有些过度设计，这次借着这个机会试试其他架构）
### 变更：
  - 自删除动画从python改成gdscript，以此绕过pty光标位置和xterm对不上的问题
### 修复：
  - 尝试修复gdscript命令执行后导致光标偏移的bug，但没修好

## 主要进展内容

基本没进展，一直在和命令行死磕，而且完善Rimworld小工具所需的时间远比预期的多，其发挥的价值远比预期的少，说实话心态有点崩。下期我准备缓缓，暂停fastai学习，只追求在心态不崩的状态下把Terminal修好

## Terminal

本质上这是我给自己挖的坑。当时测功能的时候没多试几个命令，结果现在才发现gd命令会出问题

其核心问题是，gd命令只会影响xterm状态，但pty却以为自己还和xterm同步仍在给xterm发光标位置信息，双方的状态不一致导致了显示灾难

目前我在使用“gd命令每发一行，同步给pty发一行以#开头的命令，并在回显中过滤掉#命令及其回显”的思路，不过它的状态转移我还没想清楚，直接扔给claude只会得到水多加面面多加水的结果，所以我得好好想想再继续

### 沉迷开发Rimworld小工具

[rimworld-ordinatus-calculi Demo](https://laurence-042.github.io/project/rimworld-ordinatus-calculi/demo/)

实际上这一期又画了一半时间完善这个

然后投了一篇宣传到Reddit的Rimworld板块，一篇到Rimworld的Steam社区指南

结果前者被删帖，后者没人看……

不过我确实在实现这个的过程中学到不少东西，比如怎么描述需求更加合适、demo迭代式开发试水、plotly、界面布局设计等等，也算是不虚此行

## 瓶颈与问题清单

- Terminal的显示和pty内部状态的同步
- 剧本完成后，我意识到设计当初根据大纲写的恢复程序框架有点死板了，下一期我得花大力气搞定这些交互式演出的Python脚本，其中一些还得用eval来保证玩家体验


## 下期计划（Next）

- [ ] 修好Terminal


## 试玩版

预计第一个可玩版本将在第二章的第一个涉及外部编程的游戏内容完成后推出