+++
date = '2025-11-06T10:03:00+08:00'
draft = true
title = 'Proxyos Weekly 004'
slug = 'proxyos-weekly-004'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 又停了一天电，还有一天不舒服咕了，进度延迟……主要进展为进行了完整游玩测试，修了一大堆问题，优化了一堆组件

## 本期目标

- [x] 跑一遍以确保基础的存档功能正常工作
- [ ] 把第一章的脚本要写哪些搞清楚
- [ ] 把第一章的切换逻辑搞定

## 进展速记（Changelog）

### 新增：
  - 上期新增的支持数据段和链接的文本组件现在支持Markdown了
  - 新增了两个任务之间过渡的动画
### 变更：
  - 优化任务系统，修正了可能导致稳定性下降与性能下降的不一致逻辑
  - 优化窗口系统，现在打开窗口时窗口大小取决于屏幕大小，更加自然
  - 优化存档系统，需要后台运行的应用现在都使用Manager+Display的模式了，Manager管理存档和数据更新，Display根据更新信号来修改显示
  - 优化通知系统，统一了消息对话框样式
  - 优化链接处理模块，现在它更好配置了
### 修复：
- 存档保存异常
- 存档加载异常
- 文本查看器不知道啥时候没法滚动
- 拖动数据段功能在上次更新样式后炸掉了
- 完成任务时出现了如下异常
  - TaskRequirementNode发出data_dropped信号
  - TaskManager进入submit_data_segment_to_requirement方法
  - submit_data_segment_to_requirement中check_and_update_task_status时，解锁了下一个任务，任务解锁时发出了task_updated信号（下一个任务）
  - submit_data_segment_to_requirement中check_and_update_task_status后的下一句又是发送task_updated信号（当前任务被完成）
  - Pocket在接到下一个任务的task_updated时触发了NavigationWindow的内容更新，创建了一个TaskContent，但因为其初始化方法通过call_deferred调用，新的TaskContent还没有初始化，而旧的TaskContent也还没有删除
  - 新老两个TaskContent接到完成任务的task_updated，因为新TaskContent还没初始化，发生了异常

- 进入第一章的对话框文本显示异常

## 主要进展内容

进行了完整游玩测试，修了一大堆问题，优化了一堆组件

没了

本以为上一期已经把地基打牢了，但是游玩测试中发现了远比单元测试更多的问题，比如

- 任务完成和任务发布之间没有间隔，体验十分怪异
- 默认的窗口大小（800*400）无法正常显示任务要求访问的网页
- 任务里的网页链接写错了
- 有些应用在保存未使用的存档文件，而还有些应用的存档时机不对
- 在任务完成和任务发布的间隔中，存在时序问题导致创建了异常的任务详情节点
- 默认的文本框组件单行文本过长时不会换行

除此之外，我发现一开始我把 Desktop 当成主场景有些欠考虑了，因为第一章的场景并不在Desktop上发生，需要一个新的场景（或者直接用TaskManager加载覆盖Desktop的第一章场景？）

下一期我会优先写好剧本，然后按照剧本进行相关功能的检查与开发，避免再次像本期一样把时间浪费在返工上

## 瓶颈与问题清单

暂无

## 下期计划（Next）

- [ ] 把第一章的剧本搞清楚
- [ ] 把第一章的切换逻辑搞定

## 试玩版

暂未达到第一个试玩版的发布标准