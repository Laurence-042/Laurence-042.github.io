+++
date = '2026-07-20T10:05:00+08:00'
draft = false
title = 'Proxyos Weekly 078'
slug = 'proxyos-weekly-078'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 修复了翻译流水线的一些问题，重构了 godot 侧和 mod 侧的数据交互使其不直接依赖 serde

{{< toc >}}

# 本期目标

- [ ] 修 bug
  - [ ] mod 数据加载
    - [ ] overlay 合并
    - [ ] 网页 route
  - [ ] 基于 SpiderView 的 mod 自定义 AppView 冒烟
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

这期的核心依然是完成主流程冒烟，即直接玩完第一章

但只有 2 工作日的话，我想发现 i18n 所有问题本身就是一个挑战了

**结果：**

日……serde 一堆问题

修好后 Mod 数据加载看着没问题，但是表现上似乎啥 mod 数据都没加载，下期再处理

## 本期确定性变化

### 新增：

- 添加了一些支线任务设计
- 添加了通用翻译机制，对于不受 sdk 管理的文件，开发者可以通过提供 yaml 配置翻译范围和翻译字段，并指定翻译字段的 key 的模式（支持使用类似`$.replyList[?(@.floor == ${replyFloor})].author`的动态 jpath 来让翻译器生成`$.replyList[?(@.floor == 1)].author`之类的 key 来引用字段）

### 变更：

- 替换 ForgeJSONGD 为 Godot-Object-Serializer，因为前者的 enum 处理存在严重问题——它 serde enum 时 serde 的是 enum 的 key，这和主流 json serde 的库实现完全不同，进而导致了反序列化失败。还好我有先见之明用 JsonPersistence 隔离了项目里的 serde 调用和具体库，我就猜到可能出这种问题
- 

### 修复：

- 修复翻译流水线因为 md 解析有问题，无法正确定位 rag 匹配文段的 bug
- 修复 rag 阈值过低导致假阳性过多的 bug
- 修复了 mod 侧的环境准备阶段不连 godot 侧，导致 godot 侧以为其启动超时报错的 bug（通过在环境准备阶段前连接 godot 的方式）
- 修复了 mod 正式加载时调 venv python 无法正常加载 ssl 的 bug（详情见`python 竟然出问题了……`一节）
- 修复 async 工具包在 await all signals 的时候，如果其中一个 signal 有参数会报错的 bug
- 修复 codex 搞错的 json 格式……tmd 把 PackedStringArray 给我当 string 写了
- 修复 Godot-Object-Serializer 里对于 null 的处理异常
- 修复重复反序列化导致的解析错误

### 删除：

- 

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## python 竟然出问题了……

简单来说，发生了一件看起来十分离谱的事

- 最初是发现 mod 框架启动失败
- 检查报错，发现是因为 ssl 加载失败
- 进一步验证，发现 cwd 在 embed 里就都能正常加载，但在 venv 里的就不行
- 进一步验证，发现虽然 embed 的`_ssl.pyd`和`python.exe`放一起，但 venv 的 Scripts 里明明也有 ssl
- 懵逼，找 claude

最后 claude sonnet 5 一通定位，发现是 **Windows 注册表 `PythonPath` 污染**：

- 我的 PC 装了 Miniconda，版本恰好也是 3.13，被注册进了 `HKLM\SOFTWARE\Python\PythonCore\3.13\PythonPath = D:\miniconda3\Lib;D:\miniconda3\DLLs`。
- Embed 根目录的 `python.exe` 旁边有 `python313._pth`，天然隔离这个注册表查找——所以用 embed 启动的环境准备流程一直没事。
- `uv venv` 复制出来的 `python.exe` 旁边**没有** `._pth`，于是会读取这个注册表键，把 miniconda 的 `Lib`/`DLLs` 塞进 `sys.path`（排在 venv 自己的目录**之前**）。`import _ssl`/`_decimal`/`_ctypes` 时 import 系统先撞到 miniconda 那份不兼容的编译扩展就直接报错，不会继续往后找 venv 里正确的那份。
- cwd 之所以"看起来"有关系：`sys.path[0]` 就是 cwd（`''`），cwd=Scripts 时它排在污染条目前面能抢先命中正确文件，换个 cwd 就抢不到。

claude 用终端测试证伪了 `os.add_dll_directory`和 `PYTHONLEGACYWINDOWSDLLLOADING=1`（都不能修复），又直接查注册表证实了污染源，然后验证了修复方案确实可行。

我不得不佩服，这玩意不是 python 大神真没法搞定，而我显然只是把 python 当方便的脚本语言用的，完全没深入了解。

对于非 claude 的 AI 辅助编程，那确实只是减少搬砖，但对于 claude 的 AI 辅助编程，是真的能力升级。

## 爆改 serde

### 旧的问题

最开始是发现 ForgeJSONGD 的 enum 处理存在严重问题——它 serde enum 时 serde 的是 enum 的 key，也就是说类似下面的定义

```gdscript
class EnumDTO:
	enum State { IDLE, RUNNING, DONE }
	var state: State = State.IDLE
	var label: String = ""
```

它会把这个类的默认对象序列化成
```json
{
  state: "IDLE",
  label: ""
}
```

这和主流 json serde 的库实现完全不同，进而导致了反序列化失败。

还好我有先见之明，早就猜到可能出这种问题，用 JsonPersistence 隔离了项目里的 serde 调用和具体库，因此我可以非常方便地替换成 Godot-Object-Serializer

但换完之后又发现这玩意无法很好地处理嵌套类型……

最后我放弃了，改用自己手搓，新的 serde 架构如下

### 新的架构

创建一个 Serializable，作为 可 JSON 序列化数据结构的契约基类。

所有跨 JSON / IPC / 存档边界的数据结构都应直接或间接继承本类。反序列化由
[code]SerializableSerde[/code] 目标类型驱动：调用方提供一个已 [code]new()[/code]
出来的对象，serde 反射其 [code]@export[/code] 声明属性并按声明类型从 JSON 填充：

- 同名基础属性 / Variant：直接赋值。
- Serializable 子类属性：[code]new()[/code] 后递归 [method init_with_json]。
- 有类型的 Array / Dictionary：按元素 / 值类型递归。
- PackedXxxArray 等内置容器：按结构初始化（new + append）。
- Color / Vector2 等内置值类型：按 [code].._type[/code] 信封还原。

JSON 中无法对应到任何声明属性的键（含历史 [code]__class_name__[/code] 标记）会被
静默忽略，因此 mod 作者撰写的纯 JSON 与 Python 侧仍带 [code]__class_name__[/code]
的 DTO 都能被同一套规则消费。多态集合（如 [code]Array[ChapterEventAction][/code]）
不再依赖标记派发，而是由持有它的类的 [method init_with_json] 显式解析子类。

子类按需重写 [method init_with_json] / [method export_to_json]：先处理需要特殊处理
的键（处理后从 JSON 删除），再调用 [code]super[/code] 走默认反射。

### 架构设计背景

实际上，一开始过于依赖 serde 本身就是个设计缺陷

因为 mod 侧的数据结构本身就该是稳定的抽象数据配置，godot 侧的数据结构可能会随着开发做各种优化与迁移，两者用 serde 交互反而会导致强耦合

所以真正合适的方式是将 mod 侧数据真正当抽象数据配置，然后让 godot 各个组件按照自己的需要去解析它们

serde 在这个过程中只是个方便的 util，而不该什么都依赖 serde

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- mod meta、mod list、pylock.toml、依赖安装与版本回滚之间还需要形成稳定流程，否则后续 mod 管理会变成新的技术债。
- 为啥数据看着加载了但是没生效

# 下期计划

- [ ] 修 bug
  - [ ] mod 数据加载
    - [ ] overlay 合并
    - [ ] 网页 route
  - [ ] 基于 SpiderView 的 mod 自定义 AppView 冒烟
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