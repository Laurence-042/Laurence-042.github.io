+++
date = '2026-04-23T10:28:00+08:00'
draft = false
title = 'Proxyos Weekly 053'
slug = 'proxyos-weekly-053'
series = ['proxyos-weekly']
categories = ['ProxyOS', 'DevLog']
tags = ['ProxyOS', '周报', '独立游戏开发', '技术日志']

+++

> TL;DR 概览
>
> 第一章系统基本完工，大幅改进了脚本执行系统

{{< toc >}}

# 本期目标

- [ ] 把 demo 从 alpha 打磨到 beta
  - [ ] 第一章南，然后使用一个独立的、默认启动的程序来带着玩家敲一遍，完事之后再让玩家用 diagnose 和 manual fix。 
    - [ ] 【低优先级】xterm 的 col 似乎计算不太对劲，有时候一行末尾的字只显示了一半，需要看下 xterm 实现，必要的话进行修复
    - [ ] 【低优先级】xterm 的 cursor_pos 在 cursor 不在视野内时返回末行 pos 是个 bug，而且在外面基本没法绕，只能修 xterm
    - [ ] 重新实现第一章的系统
      - [x] 内部编辑系统测试
      - [ ] 我应该还需要在恢复演出脚本里额外加个变量存在性检查，在玩家输错的情况下帮助快速定位问题
      - [ ] 需要添加 exception 转译，把异常翻译成人话，避免 indent 和 not defined 之类的搞晕玩家（而且说实话它们确实对初学者不友好）
  - [ ] 第二章
    - [ ] 将编程手册提前到第二章开始，而不是第一个任务完成后
    - [ ] 调整文案以适应安全内核的角色调整
  - [ ] 优化剧本系统架构，使存档系统以其为核心，每个 Event 完成后才存档，以此保证 Trigger+Actions 组成的 Event 的原子性
- [ ] beta 打磨完成后
  - [ ] 开个 itch
  - [ ] 琢磨下宣传
# 进展速记

## 本期假设 / 预期

**预期：**

说实话，我不太想动 xterm……

因为新的架构下我其实不太需要真正的、能处理所有控制序列的终端，而且我也没打算让玩家自己去写需要操作控制序列的终端应用

所以本期关键是完善第一章系统

**结果：**

搞定了，虽然第一章系统状态比我想象得糟糕，但经修复，其核心功能都以合理的状态完成了

## 本期确定性变化

### 新增：

- 

### 变更：

- 优化了内部编辑器架构，现在编辑更加直观且受控了
- 优化了第一章的执行，现在逻辑更加清晰
- 对 ScriptExecutor 进行了重大更新，现在它可以支持调试功能了
- 为本质上是 ScriptExecutor 冒烟测试的 Boot 动画添加了对 IPC 等更详细的测试，并将其主要逻辑分离出 Terminal 模块以提高可维护性

### 修复：

- 修复点击空白处时，编辑不 commit 的 bug
- 修复了没有错误时反而会因为获取不到错误而报错的 bug
- 修复了第一章人任务无法正常完成的 bug

### 删除：

- 

# 主要进展内容/本期关键判断点

> 我做出了哪些「如果错了也要付代价」的判断？

## 原型设计模式似乎没有如预期工作

原因有很多，这导致内部编辑器的完善速度严重减慢

### Claude 傻了

即使是 Claude Opus 4.7 也在抽风，最近一周尤为严重，sonnet 4.6 几乎降智成 chatgpt 了

> 虽然我嘴上这么说，但实际上 sonnet 4.6 还是断崖领先 GPT-5.3-Codex 的。前者只是开始搞不定复杂逻辑，但你还是能看出来它在努力搞定。而后者简直糊弄学大师、屎山创造者、架构破坏 MVP

于是我不得不降级我的工作循环，把更多的精力花在描述模块甚至方法的内部逻辑实现思路上，以保证其实现符合预期

就比如说本期的麻烦：内部编辑器

实际上，上期已经进行了一轮爆改，内部编辑器已经基本可用了，但是因为我没有描述“一行里可以有多个可编辑点”，所以 Opus 4.7 实现时直接假设其必然由`<不可编辑前缀><可编辑><不可编辑后缀>`组成，并以此为基础进行了爆改

说实话，我觉得“让一行支持多个可编辑点”是理所应当该考虑的，而且即便真的最多只有一个点，那也该用 array 存储一行中的多个片段，以供后续扩展——因为这种实现起来反而比写死三段更方便。

以前即使我不明说，Opus 4.6 甚至 sonnet 4.6 也都会自己意识到需要这么写，但现在花费是 sonnet 4.6 的 7.5 倍的 Opus 4.7 都栽坑里了，所以我真没招了，我只能去自己描述算法了。

你要问我为啥不直接让模型进一步修改（毕竟 context 就是干这个的对吧），但我只能说，我试过了

一开始我和以前一样说

```
code_row 和 internal_editor 的 prefix 和 suffix 应该没用了吧？毕竟 internal_editor 只需要维护 code_row 的 array，code_row 只需要维护 code_segment 的 array
```

但我发现模型完全没有正确理解，它以为自己要把只在某个函数里使用的成员属性内联到函数里

然后我就在否定它先前的解法后说

```
我们完全可以直接让 internal_editor 直接按行切分 template，每行调用 code_row 的 build，然后 code_row 里面直接操作 segments
```

然后我发现它还在坚持 prefix、suffix

于是我只能再次否定，几乎完全在描述算法
```
更详细地说，我们完全可以这样：

- internal_editor 按行切分 template，instantiate 一个 code_row，将 template 一行和“MARK 是否未闭合（默认状态传闭合）”传入，并要求得到一个“MARK 是否未闭合”的处理结果
    - （如果传入的表示未闭合，则跳过这一步）code_row 寻找 MARK_START，- 没找到的话就直接一个 readonly，然后返回闭合
    - 找到 MARK_START 的话，把找到位置之前的做 readonly，然后寻找 MARK_END，没找到的话就把剩下的部分作为 editable，然后返回未闭合
    - 找到 MARK_END 的话，就把找到位置之前的做 editable
    - 然后再次找 MARK_START 继续处理（本质上就是回到 code_row 的第一步），直到传入的 template 行处理完成
- 对每一行 template 依次创建新的 code_row 实例，并将行和前一次返回的“MARK 是否未闭合”传入其中本质上就是回到 internal_editor 的第一步），直到传入的 template 处理完成
```

心累，手也累

### 指令遵从性也下降了

是的，就算是上面的那一整套算法口述，Claude Opus 4.7 照样没遵从，还是在那折腾它的 prefix 和 sufix

甚至我再次

```
internal editor 的_before_context_lines、 _after_context_lines、_has_mark 都不该在当前算法下存在，而_initial_editable_template_lines 也应该只在构建方法里存在。请重新审视计划，并严格按照计划实现
```

并再次附上核心算法和实现计划后，它还是没照做

### 需要哄着它？

我实在没招了，于是几乎在自暴自弃地

```
不对，按照算法，InternalEditor 除了切分 Template 字符串为字符串数组之外，根本不应该有任何解析行为
咱俩到底哪里沟通出问题了？
```

然后它确认自己的实现确实完全偏了，并向我重新确认了方案

然后就好了，它开始正常工作了

我怀疑这是 LLM 的训练本身就使其对“维护自己所说的事物的一致性”的权重更高，类似“用户可能会突然胡言乱语所以可以不听，但我不能胡言乱语所以自己吹的牛必须圆上”的感觉。

或者更可能的原因是，当它在获得我的输入后，需要先查看当前代码才能开始实现。但在查看之前错误实现的代码时，被大量代码中的大量不符合当前方案的描述干扰了，而这些描述不仅 token 量远多于我的输入，还占据了 context 的末尾。这就导致我的输入没有得到足够的注意力，反而那些错误描述得到了更多注意力，进而导致实现偏差。但是当它自己开始确认方案的时候，它的方案描述本身就有很多 token，而此时其先前看的代码也被新出现的方案描述挤到了 context 的中间，方案描述也成了 context 的末尾，这就导致它的方案描述和我的对方案的二次确认和调整得到了足够的注意力，进而开始遵循方案。

所以下次我在进行大规模重构时，我会要求模型看代码，然后让它给个方案，接下来我再给我预期的方案，最后在与模型讨论、整合、确认这个方案后，再要求模型实现。因为模型可能不会再重复看代码，这样就能保证注意力较多的 context 尾部是正确的方案，而不是错误的历史实现。

而事实证明我这个方案确实是对的，至少从我的主观感受来看，随后的重构中 Claude 的指令遵循度得到了极大的提升

## 预期之外的 bug

我使用了类似如下架构来制作那个编辑区受限的游戏内代码编辑器

- InternalEditor 内部编辑器
  - CodeRow 代码行
    - ReadonlyCodeSegment 不可编辑的代码
    - EditableCodeSegment 可编辑的代码，点击后转换成包含 LineEdit（也就是 HTML 里的 input）的 EditingCodeSegment，在确认编辑后（解除 focus）会转回 EditableCodeSegment
    - ReadonlyCodeSegment 不可编辑的代码
  - CodeRow

然后出现了 bug：

- EditingCodeSegment emit backspace_on_empty
  - 这个信号用于通知 CodeRow，它里面有个 Segment 被删完了
- CodeRow _on_editing_backspace_on_empty emit delete_requested
  - 这个信号用于让只有一个被删完的 Segment 的 CodeRow 通知 InternalEditor 这个 CodeRow 可以被移除
- InternalEditor _on_row_delete_requested _editable_area.remove_child(row)
  - 于是 InternalEditor 移除了这个 CodeRow
- CodeRow 里的 EditingCodeSegment _on_focus_exited emit committed
  - 但因为 focus 还在之前的 EditingCodeSegment 里，而 CodeRow 的移除导致它失去了 focus，于是它通知 CodeRow 把自己换成 EditableCodeSegment
- CodeRow _on_editing_committed _swap_to_display(source_segment)，_configure_editable_segment
  - 于是 CodeRow 就这么换了
- _swap_to_display 创建的 EditableCodeSegment 不会 ready，但被要求 configure content font，然后访问 content null 了
  - 在换的时候，CodeRow 同步设置了字体、字号之类的信息，但因为 CodeRow 已经在被移除了，所以 EditableCodeSegment 不会 Ready，其子节点也不会 Ready，结果 EditableCodeSegment 访问子节点来设置字体、字号时就 null 了

我的解决方案是在“CodeRow 里的 EditingCodeSegment _on_focus_exited emit committed”这一步将其阻断，让 EditingCodeSegment 发 committed 信号前先等 1 帧，然后检查自己在不在节点树里，如果不在的话那就直接不发 committed 信号

说实话，我也试过更符合直觉的“让 CodeRow 在_exit_tree 的时候 disconnect 与 segments 的信号”这一方案，但实际测试后发现当 row 被 queue free 时，segment 的_on_focus_exited 先被执行，而且此时 segment 的 is_inside_tree 是 true，is_queued_for_deletion 是 false，随后 row 的 exit tree 才会被调用

我想这确实可以理解，因为 Godot 的 queue free 是在帧末尾真正 free 并让节点 exit tree，但 queue free 的时候就让 row 连带 segment 失去了 focus，问题还是发生了。思来想去好像也只有让 commit 发出前等 1 frame 来避免和 free 竞争，因为除此之外恐怕只能在 row 的各个地方加保护

我也想过要不要让 segment 在 emit backspace_on_empty 后直接自行 release focus，但仔细想想我意识到这样无非是把被 godot 触发的 focus exit 提前了而已，根本解决不了问题

所以我觉得那个看起来很 workaround 的的 await processframe 反而是最可行且优雅的

## 奇怪的脚本执行系统

简单来说，我进行了各种测试，然后发现“脚本语法错误”的情况下 Godot 侧始终拿不到对应的 debugger 响应

于是我先通过让 python 侧输出调试日志到 temp 文件的方式，确认了 python 侧发了

然后我又通过加 godot 日志的方式，确认了 godot 侧没收到

但是 godot 之前发给 python 的 debug 配置却能然 python 收到，两者分明在使用同一个 websocket channel！

妥妥的见鬼，如果我自己处理，我可能得处理两三天。但既然 claude 能正常回复了，我们还是迅速找到了可能原因：godot 可能在同一 frame 同时接到错误数据和 socket 关闭请求时，会先执行 socket 关闭请求。解法也很简单，让 connector 在退出前固定等 50ms，让最后一次上报数据和关闭 socket 分散在不同 frame 就行了

……奇怪的 bug

# 瓶颈与问题清单

> 哪些问题还没解，但也许我已经知道“它们不是什么”？

# 下期计划

- [ ] 把 demo 从 alpha 打磨到 beta
  - [ ] 第一章南，然后使用一个独立的、默认启动的程序来带着玩家敲一遍，完事之后再让玩家用 diagnose 和 manual fix。 
    - [ ] 【低优先级】xterm 的 col 似乎计算不太对劲，有时候一行末尾的字只显示了一半，需要看下 xterm 实现，必要的话进行修复
    - [ ] 【低优先级】xterm 的 cursor_pos 在 cursor 不在视野内时返回末行 pos 是个 bug，而且在外面基本没法绕，只能修 xterm
    - [ ] 重新实现第一章的系统
      - [ ] 细化报错反馈机制，在玩家输错的情况下让安全内核通过确认变量存在性来帮助快速定位问题
      - [ ] 需要添加 exception 转译，把异常翻译成人话，避免 indent 和 not defined 之类的搞晕玩家（而且说实话它们确实对初学者不友好）
    - [ ] 优化第一章的文案，使其更加贴合新的系统
  - [ ] 第二章
    - [ ] 将编程手册提前到第二章开始，而不是第一个任务完成后
    - [ ] 调整文案以适应安全内核的角色调整
  - [ ] 优化剧本系统架构，使存档系统以其为核心，每个 Event 完成后才存档，以此保证 Trigger+Actions 组成的 Event 的原子性
- [ ] beta 打磨完成后
  - [ ] 开个 itch
  - [ ] 琢磨下宣传

# 试玩版

暂缓，第一次上传需要做好准备，等进入 beta 阶段再说