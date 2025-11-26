+++
date = '2025-11-26T20:08:00+08:00'
draft = false
title = 'Proxyos Weekly 009'
slug = 'proxyos-weekly-009'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 这一期咕了

## 本期目标

- [ ] 完成第一章
  - [ ] 更新当前交互脚本基础框架
  - [ ] 实现六节的脚本
- [ ] 重新审视目前的章节切换流程，确保其扩展到三章时不出大问题

## 进展速记（Changelog）

### 新增：
  - 第一节脚本
  - 第二节脚本
### 变更：
  - 无
### 修复：
  - 无

## 主要进展内容

这一期基本咕了，倒不是遇到啥难题，就是单纯的麻烦，然后失去了动力效率偏低。

感觉很不爽，于是去继续搞fastai，结果被kaggle一套组合拳下来彻底干不下去了

### kaggle的组合拳

当时我在看这个fastai的官方教程
https://colab.research.google.com/github/fastai/fastbook/blob/master/09_tabular.ipynb

里面需要使用kaggle的数据，而且后面的内容都是依赖这个数据的
注册kaggle，填一堆信息，获取token，执行
kaggle 401，查了下发现是kaggle把colab给ban了
发现kaggle也提供了在线notebook执行器，但因为这个ipynb文件超过1MB不让导入
手动裁掉了文件中比较大的图片，重新导入执行
发现kaggle的环境装不了第三方依赖库，而且也不给GPU资源
只能本地搭环境，结果因为fastai和pytorch的安装顺序搞反了，导致装上了CPU版的pytorch，GPU的没装上
删除venv重新装依赖
装完依赖执行ipynb，结果发现里面使用了没列在requirements里的依赖
补装后再次执行
kaggle 403，查了下发现是kaggle要求用户签署对应比赛的同意书才能下数据
找半天没找到同意按钮，结果找了一圈后发现kaggle已经不提供加入老比赛下载老比赛数据的方式了
走投无路问ChatGPT，她说fastai的sample里可能有给了我个URL，404
再次问ChatGPT，她说github里可能有给了我个URL，404
血压拉满再次要求ChatGPT核查，她说她可以把她那里的数据给我，但需要我等下
饱含怀疑地要了数据，结果她给我发了个ChatGPT的聊天URL——还正是我问这个问题的聊天URL

血压爆了

### 沉迷开发Rimworld小工具

心态崩了之后，自然就得找发泄渠道。于是我去玩了半天Rimworld，然后发现其中两个武器我很难抉择，它们造价相差无几，但穿甲、伤害、不同距离的精度都相差很大，我没法很简单地算出哪个更适用于我的游玩风格。于是……

我去做了个Rimworld计算器

一开始只是准备给定命中率、穿甲、理论最大DPS，画敌人护甲和实际DPS的关系曲线的，结果后来越做越投入，连曲面和多层护甲都整出来了……

就这么做了两天，一看时间——哦豁，ProxyOS咕了

不过今天顺利的话我应该能把它的链接放下面

[rimworld-ordinatus-calculi Demo](https://laurence-042.github.io/project/rimworld-ordinatus-calculi/demo/)

## 瓶颈与问题清单

- 剧本完成后，我意识到设计当初根据大纲写的恢复程序框架有点死板了，下一期我得花大力气搞定这些交互式演出的Python脚本，其中一些还得用eval来保证玩家体验
  - 我确实可以去戳copilot claude，但是之前他没能很好地实现第一章的开始动画演出，而且第一节写得也有不少问题，扯皮两三轮后还是手改了一堆


## 下期计划（Next）

- [ ] 完成第一章
  - [ ] 更新当前交互脚本基础框架
  - [ ] 实现六节的脚本
- [ ] 重新审视目前的章节切换流程，确保其扩展到三章时不出大问题


## 试玩版

预计第一个可玩版本将在第二章的第一个涉及外部编程的游戏内容完成后推出