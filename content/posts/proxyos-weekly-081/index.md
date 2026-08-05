+++
date = '2026-07-30T09:03:00+08:00'
draft = false
title = 'Proxyos Weekly 081'
slug = 'proxyos-weekly-081'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 翻译流水线彻底完成，冒烟被涉及 WebView 的演出窗口阻塞

{{< toc >}}

# 本期目标

- [ ] 修 bug
  - [x] mod 数据加载
    - [x] overlay 合并
  - [ ] 文件引用处理冒烟
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

没跑完，在 i18n 上遇到的阻塞问题有点多

都搞定后验证了翻译全流程无误，但是一些基于 SpiderView 的临时界面的渲染又出现了问题，按理说同样基于它的 Terminal 没问题就不该有问题啊……我怀疑是什么地方写歪了导致 SpiderView 的生成时序有问题

## 本期确定性变化

### 新增：

- 调整 i18n，允许 mod 使用不同的基础语言，并提供各个 mod 自行 patch 全局翻译配置以提供自定义术语表和剧本文件的功能

### 变更：

- 优化 i18n 的 rag 索引，使其假阳性更少的同时不大量减少真阳性
- 优化 i18n 的 speaker 提取，使 sdk 支持提供默认 speaker 用于处理没有显式 speaker 的数据，使配置式翻译提取支持提取 speaker
- 优化 i18n 的操作，消减命令的变种，让其更符合直觉
- 优化 i18n 的目录结构，把翻译 csv 都和相关模块放一起

### 修复：

- 修复 i18n 的剧本 rag 原文索引解析器会将紧随标题的表格视为标题一部分的 bug

### 删除：

- 清除以前 i18n 架构生成的冗余文件

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## 我真的 tmd 服了 codex 了

### 进程管理一坨屎

问题：
翻译流水线的写入文件阶段报
```
error: [Errno 22] Invalid argument: 'D:\godot_workspace\proxyos\Mods\Core\Domains\cybertaoism.team\frontend\pages\outsourcing-recruitment\temp-42\_index.html.locale.csv'
```

codex：

```markdown
这不是 `_index.html.locale.csv` 内容或路径非法，而是 Windows 上一次瞬时的“截断重开文件”失败。

诊断证据：

- 每次失败的 CSV 都不同，排除固定坏文件。
- 文件存在、可写，属性正常。
- `os.open(..., O_WRONLY)` 和文本 `r+` 能立即打开。
- `Path.open("w")` 失败；等待 50ms 后同一操作成功。
- 一次完整提取中捕获了 2 次该竞态，重试后处理完 221 个文件。

`"w"` 在 Windows 上相当于以 `CREATE_ALWAYS` 打开并截断现有文件，这与普通的 `OPEN_EXISTING` 是不同路径。[Microsoft CreateFile 文档](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea) 也区分了这两种行为。结合随机文件与短延迟恢复，基本可以确定是 Defender、杀软、索引器或其他文件系统 minifilter 在“刚读取、立即截断重开”时产生的短暂竞态；目前无法仅凭 Python 异常确认具体是哪个驱动。

信息不足则是工具自身的问题：

- [csv_store.py](D:/godot_workspace/proxyos/Mods/_tools/i18n/lib/csv_store.py:252) 直接用 `"w"` 重写每个 CSV，即使内容没变化也会重写。
- [i18n.py](D:/godot_workspace/proxyos/Mods/_tools/i18n/i18n.py:403) 捕获整个 `OSError` 后只打印 `str(error)`，把 traceback、当前 source、操作阶段和重试信息全部丢掉了。
- 提取也不是事务性的：报错前面的 CSV 可能已经写完，所以失败后需要重跑。

短期可以直接重跑，通常会在另一个位置或直接成功。正式修复应该是：

1. 内容未变化时不写文件。
2. 先写同目录临时文件，再 `os.replace()`，避免直接截断目标。
3. Windows `Errno 22` 做有限重试，例如 50ms、100ms、200ms。
4. 最终错误输出 source、locale CSV、操作、尝试次数、`errno/winerror`；verbose 模式保留 traceback。

本次只做了临时诊断，诊断脚本已删除，正式 i18n 工具没有修改。
```

我：
（停止 codex 应用）

问题消失了

### 沙箱管理也一坨屎

`core.pot` 突然无法打开了，检查后发现

Owner: CodexSandboxOffline
AreAccessRulesProtected: True

也就是 Codex 创建/替换 `core.pot` 时，因为桌面端沙箱或文件替换流程的权限处理缺陷，不但成为了所有者，还莫名其妙关闭了 ACL 继承并删除了我的访问权限……

## i18n……

我知道这玩意我快折腾半个月了，但是这玩意属实是个麻烦活

本期的关键变更其实就这两条：
- 让 mod 作者可以更方便地用翻译流水线翻译自己的 mod
- 让翻译流水线内的概念一致、基础设施一致

但前者涉及了
- 翻译流水线的 Mod 级自定义
- 命令粒度的易用性
- 各种 Mod 级非代码非资源的设定集类文件如何管理与使用
- 保证流水线可靠性避免因为异常设定集写法挂掉

后者涉及了
- godot 侧翻译和 mod 侧翻译的基础设施统一
- 概念的一致性统合
- 相关文档的可读性保证

这些玩意属实是不做不知道一做吓一跳……

但好歹这次算是真完事了，之后如无意外应该不用再动它了

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- mod meta、mod list、pylock.toml、依赖安装与版本回滚之间还需要形成稳定流程，否则后续 mod 管理会变成新的技术债。
  

# 下期计划

- [ ] 修 bug
  - [ ] 文件引用处理冒烟
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