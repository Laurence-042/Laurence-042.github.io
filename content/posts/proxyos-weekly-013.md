+++
date = '2025-12-10T17:32:00+08:00'
draft = false
title = 'Proxyos Weekly 013'
slug = 'proxyos-weekly-013'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> ANORA的前端核心逻辑已经完成，初步调试无误，也具备了通过 wry 节点与 gdscript 交互的能力

{{< toc >}}

## 本期目标

- [ ] 完成逻辑图系统，考虑用TypeScript+Vue/React之类的搞一个ANORA原型，然后通过wry集成进游戏，通过wry的事件系统进行操作
  - [x] Node框架
  - [x] 分层Port
  - [x] Connection折叠/展开
  - [x] 逻辑图计算
  - [x] 简而言之就是之前的AWW的所有除了定制节点之外的基础计算和显示逻辑，时间有点紧，毕竟这些东西当时我用了好几个月内的工作间隙。但我觉得有善用claude应该能及时完成——Again
  - [ ] 集成进游戏
    - [ ] 无UI模式（纯逻辑图，游戏内通过GDScript控制）
    - [ ] 适配相关关卡脚本

## 进展速记（Changelog）

### 新增：

- ANORA 核心实现
  - 虽然看起来只有一条，但改的是真的多啊
- ANORA 扩展 mod 加载

### 变更：

### 修复：

## 主要进展内容

NORA的前端核心逻辑已经完成。将上周遗留的设计问题收尾后，本期对ANORA进行了实现。

### 相较于其前身 AAW 的核心升级

- 更灵活的节点执行控制
- 更高效的计算
- 可扩展的Node、Port甚至Executor
  - 实际上核心的定义哦都是通过扩展机制加进来的
  - 所以说Rimworld的那个名为Core的mod真是个天才的构想

### 距离接入 ProxyOS 仍需完成的内容

- 无UI模式(纯逻辑图，游戏内通过GDScript控制)
    - 初始化图
    - 控制按步执行
    - 一些为了通用的动画演示准备的画面效果
- 适配相关关卡脚本
  - python脚本输出特定指令控制GDScript控制逻辑图

## 瓶颈与问题清单

- 暂无

## 下期计划（Next）

- [ ] 无UI模式(纯逻辑图，游戏内通过GDScript控制)
    - [ ] 初始化图
    - [ ] 控制按步执行
    - [ ] 一些为了通用的动画演示准备的画面效果
- [ ] （有时间的话）适配相关关卡脚本
  - [ ] （有时间的话）python脚本输出特定指令控制GDScript控制逻辑图

## 试玩版

预计第一个可玩版本将在第二章的第一个涉及外部编程的游戏内容完成后推出