+++
date = '2026-07-27T10:04:00+08:00'
draft = false
title = 'Proxyos Weekly 080'
slug = 'proxyos-weekly-080'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 冒烟测试继续推迟。本期统一了 Terminal 与 SpiderView 架构，改善聊天与 i18n 工作流，并形成了以模块级结构化 `AGENTS.md` 控制 LLM 文档质量的方法。

{{< toc >}}

# 本期目标

- [ ] 修 bug
  - [ ] mod 数据加载
    - [ ] overlay合并
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

没跑，在调qol，而且i18n也还有问题

## 本期确定性变化

### 新增：

- 添加了可选的“通过后续消息来取消之前已经计划且尚未发送的消息”的特性，用于平衡长对话和快处理，避免玩家提前完成任务时会出现的npc的任务间、任务后发言混杂的问题

### 变更：

- 将terminal的架构和SpiderView统一
- 通过滚动缓动来优化聊天界面的表现
- 整理IPC与SPIDER模块的文档为稳定`AGENTS.md`
- 调整i18n流水线的extract-gettext，使其只扫描真正的后端代码，避免扫描资源文件，且优化了其生成文件的格式，避免其报各种警告
- 优化i18n排序机制，使其条目顺序和文本出现顺序一致

### 修复：

- 修复基于SpiderView的Terminal没有被正常加载的bug
- 修复主动向Terminal里写数据会因为CRLF和LF的差异而产生非预期缩进的bug

### 删除：

- 

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

这期没啥可说的，因为本质上这期的原计划没有进行，工作重心转向基础设施和维护机制，而这俩也没啥特别值得说的

唯一值得说的也就只剩——

## AGENTS.md

这期我去看了些LLM大厂开源产品里的`AGENTS.md`，想从中学点经验，好让我能不再被codex之类的气到破防

### 大厂是怎么做的

但出乎我意料的是，其中几乎没有统一的模式，甚至即使是同一个厂的不同产品里`AGENTS.md`的模式也大相径庭

- https://github.com/google-gemini/gemini-cli/blob/main/GEMINI.md
  - 内容：基本就是`README.md`
  - 格式：各个模块的子文档都很短，且没有固定架构，唯一共同点就是都写了目录里的各个文件是干啥的
  - 限制：不少模块的子文档都跟打地鼠直接写“不要xxx、不要yyy”
  - 风格：看不出啥固定风格，就是极简markdown
- https://github.com/google/go-github/blob/master/AGENTS.md
  - 内容：几乎只有一行“去看`CONTRIBUTING.md`”，而那个文件里主要是各种代码模式示例
  - 格式：就是一个正常的`CONTRIBUTING.md`，法律要求、pr要求、测试要求、代码示例
  - 限制：主要由代码示例提供，看起来这是个进入维护阶段、主要是横向扩充的项目，基本就是在教贡献者如何用仓库里的代码模式
  - 风格：标准大厂开源项目的`CONTRIBUTING.md`
- https://github.com/google/adk-python/blob/main/AGENTS.md
  - 内容：除了每个核心模块的一句话介绍外，就几乎只有一行“看你的skill”。skill里看着主要是“什么情况下读什么”的内容路由
  - 格式：基本是“这里有什么”和“什么情况下读取”
  - 限制：基本都是“应该按什么路走”和“走的过程中的自检项”，只在涉及commit之类的部分有用语风格要求
  - 风格：感觉像是机修手册。基本模式是“可以咋做”、“有哪些变种”、“检查项”、“示例是什么”
- https://github.com/openai/codex/blob/main/AGENTS.md
  - 内容：一团乱麻，把后知后觉的打地鼠、rust编程规范、CI操作方式之类的和项目要求完全混一起了。进一步检查还发现有很多段落出现了重复
  - 格式：看起来是想到哪写到哪，比如下面这段就是它的项目级`AGENTS.md`的目录
    - Rust/codex-rs
      - The `codex-core` crate
      - Code Review Rules
        - Crate API surface
        - Model visible context
        - Breaking changes
        - Test authoring guidance
        - Change size guidance (800 lines)
      - TUI style conventions
      - TUI code conventions
        - TUI Styling (ratatui)
        - Text wrapping
      - Tests
        - Test module organization
        - Snapshot tests
        - Benchmarks
        - Test assertions
        - Spawning workspace binaries in tests (Cargo vs Bazel)
        - Integration tests
          - codex_core integration testing
          - app-server integration testing
      - App-server API Development Best Practices
        - Core Rules
        - Client->server request payloads (`*Params`)
        - Development Workflow
      - Python Development Best Practices
        - Ignore Python 2 compatibility
      - Platform Support
  - 限制：打地鼠现象比gemini的还严重，通篇都是
    - 不要碰沙箱变量；
    - 不要调用 `reset_client_session`；
    - 不要继续往 `codex-core` 里堆东西；
    - 不要向几个大型 TUI 文件添加方法；
    - 不要写超过 800 行的修改；
    - 不要生成超过 10K token 的上下文片段。
  - 风格：明显ChatGPT写的，其臭毛病在这个文档里体现得淋漓尽致

### 我是怎么做的

看了这么些之后，说实话有个模糊的感觉，但具体应该咋做还是没有定论

首先我确定了我不该咋做

- 不能打地鼠
- 不能和OpenAI那样让ChatGPT自己给自己喂屎
- 必须分布式可维护
- 不能太消耗人力

然后我对比了四个项目里我该学的和我该避免的

- https://github.com/google-gemini/gemini-cli/blob/main/GEMINI.md
  - 别打地鼠
  - 明确目录结构也许是好的，但按我这段时间的经验，靠谱的llm自己会从文件名和引用关系看出来，直接写反而经常因为过于简略而让llm误判
- https://github.com/google/go-github/blob/master/AGENTS.md
  - 作为横向扩展的维护项目这么搞应该可以，但对于经常变的持续开发项目来说不合适
- https://github.com/google/adk-python/blob/main/AGENTS.md
  - 分布式skill是个好想法，但维护有些耗人工
  - 我最好用能让llm自行随功能变更通过string find找到文档过时点进行更新的结构，而不是这种需要深度索引的
- https://github.com/openai/codex/blob/main/AGENTS.md
  - 纯屎

于是我的方案开始清晰：

- 为了避免人工复杂，模块级`AGENTS.md`就是最优解
- 为了保证信源可靠，人工写方案决策草案总是不可避免的。那么“人工写草案，然后llm检查，人工完善后llm执行，最后根据实现结果结合最初的决策让LLM写`AGENTS.md`”这个工作流就是权衡之下可靠性与速度都可接受的中间态
- 为了保证llm能找到，模块级`AGENTS.md`里需要有明确的可被llm索引的段落
- 需要保证可读，避免无穷无尽的打地鼠和事故记录让文件不可读

那么方案几乎就只有一个：

**通过文档结构来限制`AGENTS.md`的内容，用结构避免LLM遗漏关键内容或者往里面拉屎**

于是我开始找有没有现成的参考，结果我找到了 OASIS Open（The Organization for the Advancement of Structured Information Standards）的 DITA （Darwin Information Typing Architecture）

其本质上是个软件和技术文档领域的结构化标准。DITA 将内容拆成带类型的独立主题，基础类型包括：

- `concept`：它是什么、如何理解
- `task`：如何完成某个目标
- `reference`：参数、属性、命令等查询资料
- 后续扩展还有 troubleshooting、machinery task 等

而其`task`要求包含如下字段

- 标题
- 简述
- 前置条件
- 背景
- 步骤
- 预期结果
- 示例
- 后续要求

我觉得其中的`简述`和`背景`已经能表达`concept`了，而`reference`在对应段落按需放就行

而这些字段本身就能避免LLM犯错

| 发现的问题                 | 对应约束                           |
| -------------------------- | ---------------------------------- |
| 文档只写“不要做什么”       | 先写职责、边界、正常流程和预期结果 |
| 内容随事故无序增长         | 使用固定但可裁剪的章节结构         |
| 复杂关系仅靠散文描述       | 对比用表格，流程与状态用 Mermaid   |
| 文档逐渐脱离代码           | 路径、字段、示例必须按当前实现验证 |
| 修改一个流程却漏改邻近资料 | 明确同步更新范围                   |

最后这一大串的结果就是，我在项目级AGENTS.md里加了这么一段

```markdown
## Documentation writing

- 首先描述对象“是什么”：明确职责、边界、正常流程与预期结果。否定式对比
  （如“不是 xxx”）仅用于补充关键风险、历史兼容或明确禁止项，并放在正向
  模型之后。
- 文档结构按内容需要从以下部分中选择，保持读者可以依次理解和执行：
  `标题`、`简述`、`前置条件`、`背景`、`步骤`、`预期结果`、`示例`、
  `后续要求`。短文档可以合并或省略无法提供额外信息的部分。
- 精确映射、多项对比和重复字段优先使用表格；涉及多个组件、分支或状态变化的
  流程优先使用 Mermaid 图表用于澄清正文难以直接表达的关系，并与正文中的
  名称和代码契约保持一致。
- 文档应提供可执行、可验证的信息。路径、命令、字段名和示例以当前实现及附近
  文件为依据；说明与实现出现差异时，以实现为准并同步修正文档。
- 修改文档所描述的工作流时，同步相关 README、生成文件、本地化输出和兄弟
  文档，使术语、链接与契约保持一致。
```

说实话我自己都觉得有点虎头蛇尾，但我也觉得这样应该就够用——因为我已经基于这个整理了一些关键模块的AGENTS.md，检视后发现效果非常不错，几乎不用手改

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

- mod meta、mod list、pylock.toml、依赖安装与版本回滚之间还需要形成稳定流程，否则后续 mod 管理会变成新的技术债。
  

# 下期计划

- [ ] 修 bug
  - [ ] mod 数据加载
    - [ ] overlay合并
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