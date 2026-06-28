+++
date = '2026-06-25T09:56:00+08:00'
draft = false
title = 'Proxyos Weekly 071'
slug = 'proxyos-weekly-071'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> mod 支持框架搭建完成，任务系统、网页系统都已经初步实现了 mod 支持

{{< toc >}}

# 本期目标

- [ ] 支线任务支持
  - [x] mod 框架
  - [x] 初步实现 mod 管理
  - [x] 任务系统 mod 化
  - [x] 网页系统 mod 化
  - [ ] 桌宠系统 mod 化
  - [ ] 信息段系统 mod 化
- [ ] 清技术债
  - [ ] lesson-runner 的 step 处理逻辑应该在 step 里，而不是在 lesson-runner 里

- [ ] 迁移现有内容中适合 mod 化的部分（基本是完整第二章）
- [ ] 将第三章开头补充进 demo
  - [ ] 调整第二章末尾文本，引入经济系统和支线任务系统
  - [ ] 通过经济系统获得通用搭载平台
  - [ ] 将 demo 结束提示放在通用搭载平台的 app 里
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

上期 agent 大失败，这次再 roll 一次 agent 鉴定

如果顺利，我应该能搞定 mod 系统的框架，并至少把任务系统搞定

**结果：**

agent 再次大失败。不过

## 本期确定性变化

### 新增：

- mod 系统框架搭建完成
- mod 化网页后端
- mod 化网页前端
- mod 化任务系统
- 为 godot-wry 添加了路由表功能，可以借此调整加载后的网页 url

### 变更：

- 调整任务系统的任务需求验证的架构，使其更加直观可维护
  - 调整任务需求的定义，合并了冗余字段，简化了任务需求的 view 的处理
  - 将验证逻辑从 Task Manager 分离到与任务需求一一对应的校验器中，避免 Task Manager 随需求类型增加而膨胀
- 优化 python 后端通过 ipc 调用 godot 侧 ChapterEventAction（本质上是游戏暴露的模块化操作接口）的方式，使其可以基于 Json 序列化适配层的机制，直接传递序列化版本的 ChapterEventAction 到 godot 侧的 ActionExecutor 直接反序列化并执行
- 将 ControlPanel（主场景）加载 ChapterController 的逻辑分离到 autoload 的 ChapterControllerManagerNode 里，以简化 ControlPanel 的逻辑，并允许 ActionExecutor 通过 ChapterControllerManagerNode
- 调整了浏览器的实现，使其 browser app、basic browser、basic webview 三层抽象的职责更加明晰
- 

### 删除：

- 

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## AI coding 工具链试错：Z.ai、Codex 与 Claude 风控

本期除了继续做支线任务和后端系统，我还被迫继续测试各种 AI coding 工具链。阶段性结论是：**能稳定使用、价格可控、并且不会破坏项目架构的 AI coding 工作流**仍然毫无头绪。

### 尝试 z.ai 的 GLM-5.2 Coding Plan

我成冤大头了。

我本来想试试 GLM 的月票，于是去 z.ai 订了 Lite。订之前我以为这只是智谱的英文官网，具体服务和国内版本应该差不多。

结果付完款才发现：

* 国际 Lite：$18，约 ¥130/月
* 中国 Lite：¥49/月

价格差异先不说，实际体验也不理想。GLM-5.2 的智力体感大概能摸到 Sonnet 一侧，但 first token latency 实在没眼看。读个文件都能卡出几分钟的等待，这对 coding agent 来说非常致命。

更要命的是，因为它太慢，我临时用 OpenRouter 救火，结果忘了切回来，今天一天直接烧了 7 美元。也就是说，原本想省钱，最后变成“订阅费 + OpenRouter 救火费”双重扣款。

而且在我准备看看中国区的会不会延迟低些的时候，发现登录完直接显示` 暂时售罄 ｜06 月 28 日 10:00 补货 `，鼠标悬停 tooltip 显示`限售期间，每日 10:00（UTC+8）释放新库存`

而我第二天定了个 10 点闹钟，并在 9:56 就去看了下，发现开始显示`抢购人数过多，请刷新再试`，然后等我终于在 10:04 刷新出新内容时，新内容显示` 暂时售罄 ｜06 月 29 日 10:00 补货 `

我的评价是卖不了就别卖

### 尝试对 Codex 做 prompt engineering

然后 Codex 的周额度恢复了。我认真尝试了一天 prompt engineering，试图把它关进更小的笼子里。

现在我确认：至少在 ProxyOS 这种项目里，Codex 的问题不是“还需要更明确一点”，而是**缺乏稳定的架构服从性**。

我确认当前使用时 Codex 自称是 GPT-5.5，effort high。但实际表现依然是：

* 跟它说最佳工程实践，它能给架空未来游戏项目的 `cert` 擅自加 `-2026` 后缀、擅自给一个正在提 pr 的第三方项目搞 cargo fmt；
* 跟它说不要擅自改无关内容，下一次让它改目录结构时，它又只改我点名的一个文件，不动同级兄弟文件；
* 跟它说多对照原始需求里的背景和目标、一切修改都要服务目标，它最后把我的需求文本当注释复制得到处都是。

这类问题不是“代码写错了”那么简单，而是它无法稳定区分：

* 需求文本；
* 设计目标；
* 当前实现；
* 应该迁移的职责；
* 不该触碰的既有命名和设定。

如果我必须把“哪个类不能动、哪个函数改 async、哪些职责下沉到哪个子类、哪些文件要回滚”写到接近代码级别，那我为什么不直接自己写代码？

~~所以 Codex 目前只能降级成机械执行工具：批量改 import、按模板补同构类、替换 Dictionary、补 Result 包装。它不适合负责架构迁移。~~

Codex 完·全·不·能·用！
力竭了，挪个目录也挪不明白，让它帮忙把 validation 合并进 proxy_os_ipc 库，我寻思这 deepseek flash 都能办明白、完全没有额外解释空间的东西能出啥问题

结果它把我引用 validation 的** validator **给**复制**走了……

---

当天晚上我意识到 codex 如果真的这么不堪应该不至于和 claude code 分庭抗礼，而且今天看到一个医学博士生在吐槽 claude 出现幻觉而 codex 能正常干活，这让我颇为困惑

于是分析后，我认为很可能是 codex 不擅长处理大上下文以及遵循现有项目架构，而 claude 不擅长在混乱的项目中保持清醒

我的理论是：科研项目有一个算一个都是屎山，这种情况下不看现有逻辑、自己搭新捷径的 codex 反而能正常实现目标（虽然本质上是在屎山上又拉了一坨）；但是 claude 会以为自己在一个靠谱项目里，而混乱的项目会让其脑补“用户这么写肯定有他的道理，虽然看着屎但也许有什么妙妙功能”，以至于出现幻觉无法正常工作

为了验证这个理论，我直接开了一个新项目。如果我的理论正确，那么即使这个项目涉及大量控件、大量文本、模糊的要求，codex 也能以可接受的水平完成它。因为它完全想咋发挥咋发挥，根本不用考虑现实项目。

实验结论是 codex 确实适合科研和非从业者做简单应用（它确实做出来了，而且就单页面应用来说结构很合理且可维护），但不适合任何需要分模块的中型应用（它依然犯了很多低级错误，比如在我明确需求“这是一个给非技术人员看的指南，其操作指示必须精确到翻译为 playwright 定位器就能直接被 playwright 执行”后，它开始给目标用户展示 playwright 定位器……我不得不用清言（基于 GLM-5.2）进行内容修正）

### Claude 风控问题

最后是 Anthropic。

我官方账号被封后，尝试过第三方成品号，结果第一次登录后不到一小时也被封了。我甚至还没开始使用 Claude，这段时间主要是在吃饭和写给 Claude 的计划书。

这说明问题很可能已经不在 prompt/output 层，因为我根本还没发任何内容。能触发风控的只剩下账号来源、付款信息、登录环境、IP 信誉、设备指纹之类我基本无法控制的因素。

这件事最离谱的地方在于：Claude Code 的协作模式确实最适合当前的 ProxyOS。它会先扫描项目、提出不确定点、整理计划，让我像 revise doc 一样批注，然后再执行。这个流程是健康的。

但如果账号可用性本身无法保证，那模型再适合也没用。

### 阶段性结论

这一轮工具链试错之后，结合之前的经验，我对几个工具的定位大致变成：

* Claude Code：最适合 ProxyOS 的架构协作，但账号风控不可控；
* Codex：动作快，但毫无工程纪律，只能做低风险机械任务；
* GLM-5.2 Coding Plan：智力尚可，但延迟让我很难把它当主力；
* OpenRouter：适合救火，但不适合无意识长时间 agent 消耗。
* Github Copilot：定价基本等同于直接用 OpenRouter

我本以为我能找到一个可以替代 6 月之前的 Github Copilot with Claude Sonnet 方案的、**能稳定使用、价格可控、并且不会破坏项目架构的 AI coding 工作流**，但目前毫无头绪

问了大学舍友里的大佬，其表示在主用 codex，而 codex 虽然有降智的时候，不过大部分时候靠谱……我在想是不是因为我不太经常让 codex 先 plan，所以它才各种偷懒。下期我准备再和 codex 死磕（话说我的周配额是不是又快没了……）

## Mod 系统初步完成

这个 mod 系统算是 demo 最后的架构变更了

其实这个上期就做了一部分，不过因为没有彻底定型所以没有详细描述和记录，这期我觉得设计层面算是基本稳定了所以来说一下

这个 mod 系统的目的是让玩家可以使用 python 实现游戏中网页的后端，并借助提供的 ipc 和 sdk 触发游戏内预设的动作，以此来只靠 mod 完成当前第二章里所有的游戏内容（实际上我正在规划将第二章的游戏内容完整迁移为 mod 体系，作为一个名为 Core 的 mod 存在——就像 Rimworld 一样）

说实话这个 mod 系统快给我整力竭了，判断点有一个算一个都是关键

### mod meta 信息 godot 侧加载还是 python 侧加载

结论：python 侧加载

python 侧在详细处理 mod 信息的时候本身就会扫 mod，让 python 侧持有 meta 信息的性能压力最小，信源更统一（虽然启动时/godot 处理 mod 管理时会需要更多交互，但相对可控，信源统一带来的维护优势更强）

更重要的是，这样以后能让 godot 侧只需要维护 mod manager view，而不必搞对应的复杂 manager。python 侧自行处理依赖安装也会更好适配。如果以后这游戏真的流行了，还能十分方便地通过 mod 来升级 mod 管理

python preflight 读出来 mod meta 后，应该做依赖版本排序，生成依赖版本快照 pylock.toml，并将旧的快照按照替换时间命名为 pylock.\<datetime>.toml 来避免玩家装依赖出问题没法恢复

python mod manager 应该优先读持久化的 mod list.txt 决定加载顺序（格式参考 requirements.txt，每行记录 modid、mod 更新地址、mod 版本，排在更前面的行的 mod 更先被加载），如果没有持久化的再使用 dag 生成 mod list.txt，最后都按照 mod list.txt 内容来做加载（保证实现只有一套）

### mod 怎么组织目录结构

结论：这个游戏的核心概念其实就是各个域名，不论是发布的任务、提供的商品、提供的信息段都依托于某个网页。不过相应的，也存在一个组织有多个域名，而组织发行了在这些域名里通用的货币的情况。因此 mod 根目录里，除了本地化和 meta 信息之外，就是`Organizations`和`Domains`两个目录，前者承载发行货币的功能，后者分成前后端承担网站功能

```
MODS
└─Core
    ├─About
    ├─locale/en/LC_MESSAGES          # 后端 gettext
    │
    ├─Organizations                   # 只放"组织级"的共享配置
    │  ├─CentralProcessingGrid
    │  │  └─org.toml                  # 声明该组织、发行的货币、cert 链
    │  ├─laurence042
    │  │  └─org.toml
    │  └─VeildNimbus
    │     └─org.toml
    │
    └─Domains                         # 域名才是核心实体
       ├─cpg.network
       │  ├─domain.toml               # org = "CentralProcessingGrid"
       │  ├─backend/                   # 后端逻辑、task、shop/stock
       │  └─frontend/                  # 前端页面
       │     ├─pages/
       │     │  └─images/
       │     └─_overlay/_en/          # 前端页面的 overlay
       ├─laurence042.com
       │  └─...
       ├─cybertaoism.team
       │  └─...
       ├─camera.home.local
       │  └─frontend/...
       └─_                             # 通用页面，为了避免混淆直接使用下划线为目录名，用于存放跨域名资源，比如需要注入页面的 js 脚本
          └─Injections/...               # 需要注入页面的 js 脚本
```

### 多 mod 共同提供一个域名的支持

结论：需要支持一个 mod 提供`proxy://A/B/C`，另一个 mod 提供`proxy://A/B/D`的情况，这是一种常见的基础 mod+内容扩展 mod 模式。但是当前逻辑需要变更

先前，mod 页面 fetch 的时候分两种情况：使用 proxy 虚拟路径，或者使用相对路径。

- proxy://虚拟路径：
  - 通过 proxied.from.unknown.architecture\spider_utils\spider_protocol_handler.js 被拦截并转化为 proxy.navigation.request
  - 进而走 web browser app 的_handle_proxy_navigation_request_
  - 走 web browser app 应该调自己的 load_url，其中会将 proxy://虚拟路径翻译成 res://实际路径，并处理 i18n overlay
  - 走 basic web browser 的 load_url，如果对应文件不存在就将对应域名的 404 页面路径传入 basic web view，存在就直接传
  - basic web view 包装的 godot-wry 的 webview 加载对应文件。`res://A/B/C` 加载后显示的 url 为 `http://res.A/B/C`（经查询其依赖的 tauri-wry 文档，确定了这个机制没法改，只要 load_url 传入的是`res://A/B/C`，就必然会这么映射）
- 相对路径
  - 在`http://res.A/B/C`访问`.。/D`的相对路径时，tauri-wry 内部自行将其作为 res://解释并访问`res://A/B/D`

为了保证 Mod 里的目录能正常组织，我为 godot-wry 引入了 res_route_table 机制，这样虽然 load_url 传入的是`res://A/B/C`，只要 res_route_table 指定`res://A/B/C -> res://E`，那么最后显示的 url 就会是 `http://res.E`

但再次检查后，发现不论 godot-wry 能不能返回其加载的目标文件是否存在（是否 404 了），最后展示对应域名的 404 页面都需要 godot 侧对 res_route_table 进行解释，所以只能改成如下别扭的流程

- proxy://虚拟路径（以访问`proxy://some-org.web`为例）：
  - 通过 proxied.from.unknown.architecture\spider_utils\spider_protocol_handler.js 被拦截并转化为 proxy.navigation.request
  - 进而走 web browser app 的_handle_proxy_navigation_request_
  - 走 web browser app 应该调自己的 load_url，其会将`proxy://some-org.web`和找不到文件时使用的 404 页面的虚拟路径`proxy://some-org.web/404.html`（项目内约定每个域名如果有 404 页，只能在根目录的 404.html）一起传进 basic web browser 的 load_url，在 web browser app setup 时，会给其 basic web browser 设置 resolver
  - basic web browser 的 load_url 接到`proxy://some-org.web`和找不到文件时使用的 404 页面的 proxy 虚拟路径`proxy://some-org.web/404.html`，并进行如下操作
    - 调用 resolver，resolver 内进行如下操作
      - 将目标 proxy://虚拟路径翻译成 res://虚拟路径，比如`proxy://some-org.web`会变成`res://some-org.web`
      - 此时 basic web browser 已经在 mod 加载时被注入了 res_route_table，按照 res_route_table 进行一次预先解释。此时 res_route_table 的内容是类似`{"res://some-org.web":"res://Mods/SomeModBase/Pages/_en/some-org.web/", "res://some-org.web/news":"res://Mods/SomeModExpand/Pages/_en/some-org.web/news"}`的做过 overlay 的路径映射的。比如`res://some-org.web`会变成`res://Mods/SomeModBase/Pages/_en/some-org.web/`
      - 文件存在就返回 res://虚拟路径，否则返回空字符串
    - 检查返回值
      - 如果存在（非空）：将返回的 res://虚拟路径传入 basic web view
      - 如果不存在（空）：将传入的找不到文件时使用的 404 页面的 proxy 虚拟路径`proxy://some-org.web/404.html`处理为 res://虚拟路径`res://some-org.web/404.html`后传入 basic web view
  - basic web view 包装的 godot-wry 的 webview 加载对应文件，此时 godot-wry 的 webview 已经在 mod 加载时被注入了 res_route_table，内容类似`{"res://some-org.web":"res://Mods/SomeModBase/Pages/_en/some-org.web/", "res://some-org.web/news":"res://Mods/SomeModExpand/Pages/_en/some-org.web/news"}`。`res://some-org.web`加载后显示的 url 为 `http://res.some-org.web`，但其内容是`res://Mods/SomeModBase/Pages/_en/some-org.web/`文件的
- 相对路径
  - 在`http://res.A/B/C`访问`../D`的相对路径时，也走通过 proxied.from.unknown.architecture\spider_utils\spider_protocol_handler.js 被拦截并转化为 proxy.navigation.request 的路（否则无法处理 404 页面）

可能会有点绕，其本质是

- web browser app：对接其他模块、提供存档机制、定制 basic web browser 使其可以处理自定义协议
- basic web browser：根据被配置的自定义协议处理器处理自定义协议，模拟 wry 的文件索引操作尝试寻找目标文件，并在找不到时显示 404。这一层也会处理历史记录、前进后退等浏览器基础功能
- basic web view：对接底层 godot-wry 的 webview 的适配层

而 basic web browser 和 godot-wry 的 webview 都进行文件索引的原因是，godot-wry 无法合理提供 404 响应码（其依赖的 tauri-wry 不提供相关接口，tauri-wry 的 load_url 是射后不管的异步启动，而其加载完成的事件没一个带 status code 的。而如果在 godot-wry 做响应缓存，又会在并发加载时混在一起，以至于工程上做不到），所以为了自定义 404 页面要么给 godot-wry 的每个 load_url 配置一个`{http_code:fallback_page_url}`，要么保证 godot-wry 别出 404——显然前者肯定不会被合入 godot-wry。我给它加个 router 那还算合理（用于部分解决需要自定义 url 的场景），但前者即使工程上没问题（实际问题很大，看起来 tauri-wry 的 load_url 没法带除了 url 之外的信息，如果要搞我就必须做 encode 拼 url 里……），那也是我的项目专有逻辑，于情于理都不该合入

所以只能在我项目里做提前校验，或者放弃单域名 404 了——但我不想放弃

### mod 提供任务，使只靠 mod 来建立核心循环成为可能

结论：

预期 mod 将使用如下流程为玩家提供游戏的核心循环内容扩展

- 玩家在各种地方获取到`pocket://task/add?source=...`链接，点击后 godot 的 pocket 的 handler 自动向 source 发 get
- python 侧对应的 handler 接到 get，调用 proxy_os_ipc.server.pocket 的方法给 godot 发消息使其激活并发放对应任务
- 玩家收集对应信息段、完成对应 python 脚本、通过脚本生成 json 结果文件提交到 remote request requirement
- godot 根据 remote request requirement 里配置的 url，向 python 侧发送玩家提交的数据、任务 id、需求 id
- python 侧对应的 handler 接到数据后，根据 mod 作者自行编写处理逻辑进行响应。
  - 目前支持的最常见的范式如下
    - 使用 proxy_os_ipc.server.pocket 封装的方法获取对应任务的对应需求的 json 校验配置
    - 使用 proxy_os_ipc.server.pocket 封装的方法比对玩家提交的 json 和需要的 json
    - 如果满足要求，通过 ipc 发 mint_coins 获取 json 校验配置里指定的货币后，构建 wallet://claim 链接 和 npc 的回复，内容类似“干得漂亮……这是你的报酬 wallet://claim……期待以后能再次与你合作”
    - 使用 action_executor 的机制让 godot 插入这条对应 npc 的 simpleChatMessage
    - 玩家点击链接，godot 弹出提示“转账已接收：CPG 币 20”（可能需要优化 scenes\wallet\wallet_manager.gd 使其支持自动发 notification）
  - 以后需要支持的范式如下，上述修改点完成后应该天然支持
    - 使用 proxy_os_ipc.server.pocket 封装的方法执行玩家提交的代码
    - 自行编写方法校验玩家脚本的输出
    - 如果满足要求，通过调整后的 action_executor 触发各种 Action（比如送新道具、将 mod 内的文件复制到玩家工作目录里等等）
    - 如此一来，任何可能的校验、可能的效果都能通过这个实现。后续规划的事件系统 mod 支持上线后，甚至能纯靠 mod 做长线游戏内容（没包含在这次实现规划中）

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- godot-wry 无法提供可靠的页面加载状态码，因此自定义 404 只能在 ProxyOS 层提前模拟文件索引。
- 多 mod 共同提供同一域名会让路径解析、overlay、404 fallback、历史记录之间的关系变复杂，不确定当前 basic browser / basic webview / web browser app 的职责边界是否已经是最佳的。
- mod meta、mod list、pylock.toml、依赖安装与版本回滚之间还需要形成稳定流程，否则后续 mod 管理会变成新的技术债。
- AI coding 工具链仍然不可控：Claude Code 最适合但账号不稳定，Codex 的表现离谱地差肯定有什么地方出了问题，GLM 延迟过高而且 tps 也很低。

# 下期计划

- [ ] 支线任务支持
  - [ ] 桌宠系统 mod 化
  - [ ] 信息段系统 mod 化
- [ ] 清技术债
  - [ ] lesson-runner 的 step 处理逻辑应该在 step 里，而不是在 lesson-runner 里
- [ ] 迁移现有内容中适合 mod 化的部分（基本是完整第二章）
- [ ] 将第三章开头补充进 demo
  - [ ] 调整第二章末尾文本，引入经济系统和支线任务系统
  - [ ] 通过经济系统获得通用搭载平台
  - [ ] 将 demo 结束提示放在通用搭载平台的 app 里
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