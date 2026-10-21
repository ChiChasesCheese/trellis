# Amazon 编码面试在评什么（按 senior 准备）

编码面试评三件事，并且要求你合在一起做到：数据结构与算法（选最高效的方案，并说明为什么）、代码是否清晰可维护（别人能读懂、能扩展）、解决问题的方式（先澄清、再取舍、再验证）。每场约 55–60 分钟，除了编码还会有行为问题，所以编码部分大约 40–45 分钟。岗位级别再低，准备也一律对标 senior（SDE II / III）：第 5 节列出了差别。

## 1. 评分标准（要做到的事）

| 主题 | 你要做到 |
|---|---|
| 代码质量 | 写出可维护、可读、可复用的代码：方法和类按职责拆开，变量、方法、类的命名让从没见过这段代码的人也能读懂、扩展、调试；不要一个函数包办一切。 |
| 语法 | 在在线编辑器里写语法正确、能运行的代码，不写伪代码。编辑器是纯文本协作工具，没有编译器；漏一个分号不会扣分，重点是把过程说出来。 |
| 需求与边界 | 先问清需求，再把它写成干净的代码；动手前列出正常用例、会让代码出错的用例、边界条件、空值，并和面试官确认。 |
| 测试 | 测试的名字应该描述业务或技术需求，测试代码与名字一致；写完用例逐行跑一遍，自己找 bug。 |
| 先跑通再优化 | 从最简单的可运行解开始，每次解决一件事；面试官追问时在原解上迭代，不要删掉重写。 |
| 数据结构与算法 | 选最高效的方案，比较几种做法并解释为什么选这个；会被追问数据结构的原理，例如「哈希表插入和查找是多少复杂度？它怎么做到？真的是 O(1) 吗？」，只背结论不够。 |
| 取舍 | 两个方案各有缺点时（很常见），选一个并说明理由。复杂度表达不必字字精确，但要说清时间和空间的权衡。 |
| 时间分配 | 三块：澄清需求并考虑情况如何演变；写出覆盖全部需求的第一版；增强方案，主动追问新需求并展示解法如何随需求演化。 |
| 出声思考 | 编码前先讲思路，边做边说你在怎样改造解法；用例子检验想法，说出你的假设并问面试官是否同意。 |
| 提示 | 没有陷阱题和陷阱提示，提示都有用，听到就记下来。不要只说「我卡住了」，要问有方向的问题。 |
| 不要过度设计 | 保持简单，不为题目没有要求的东西设计。 |
| 语言 | 选你最熟的语言；评的是计算机基础，不是某个语言的冷知识。 |

面试里的几条做法：

- 看到自己在复制粘贴一串 `if`，就该抽成函数。
- 面试官不是来评判你的，是来帮你的；保持对话，听他们的想法。
- 练习时测试失败就全删了重写，说明没有想清楚、结构也不够可扩展；面试里新增需求或发现反例时，应在原有解法上改。
- 面试官会一直问到把需求推向扩展情形，不是只要第一个解。

## 2. 把评分标准翻译成可执行动作

编码评分的 5 个准则组，各自对应你在面试里要做的具体动作：

| 评分准则 | 你要做的动作 | 在哪里练 |
|---|---|---|
| Problem solving：Ask questions | 开场 2–3 分钟问输入范围、空输入、重复、返回什么；用一个例子复述题意 | 每讲「资深追问」里的「接口 / 边界契约」条 |
| Problem solving：Justify decisions | 先说暴力解及其复杂度，再说瓶颈，再说优化；至少给出一个备选方案和取舍 | 每讲第 1 节「从最笨的解法开始」 |
| DS&A：Optimization / Shortcomings / Justification | 说出你选的数据结构为什么，以及它**在什么输入上会变差**（哈希冲突、退化成链的树） | 每讲「复杂度」与「常见 bug」 |
| Logical & maintainable：Simple / Maintainable / Organize | 函数拆分、命名、不写一个什么都干的大函数；辅助函数有单一职责 | 第 4 节的示例 |
| Working code | 写完**自己手动跑一遍**例子 + 边界，而不是等面试官问 | 第 3 节、第 6 节 |

## 3. 边写边说（How to talk while coding）

要出声思考（think out loud）。下面是一套可以直接说出口的英文句型（你说的是英文，所以这一节用英文），按阶段分：

**① 复述 + 澄清（Restate and clarify，2–4 分钟）**

- "Let me restate the problem to make sure I understand: given ___, return ___."
- "A few clarifying questions: can the input be empty? Can there be duplicates or negatives? What should I return if there is no answer?"
- "Is the input sorted? How large can n get? That tells me whether O(n²) is acceptable."
- "I'll assume ___ unless you tell me otherwise."（说出你的假设）

**② 例子 + 暴力解（Examples and brute force，3–5 分钟）**

- "Let me walk through a small example: ___. The answer is ___ because ___."
- "The brute force is ___, which is O(___). It's slow because ___ is repeated for every ___."
- "To do better I need ___ in O(1) / O(log n)... that suggests a hash map / heap / two pointers."

**③ 选方案并取得同意（Pick and confirm，1–2 分钟）**

- "I see two options: A is ___ with O(___) time and O(___) space; B is ___ with ___. Given the constraints, I'll go with A because ___. Does that sound OK?"（选一个并说明理由）

**④ 编码（Coding）**

- "I'll start with the helper that ___, then the main loop."
- 写每个关键变量时说它的含义/不变量："`left` is the start of the window; the window is always valid."
- 卡住时："I'm weighing X against Y. X is simpler but ___; I think Y is right because ___."
- 需要的函数名/参数不记得：先说出来（"I don't remember the exact name, I'll call it `___`—is that OK?"，直接说出来并问面试官能不能自己起名字和参数）。

**⑤ 自测（Test your own code，5 分钟，**不要等面试官**）**

- "Let me trace the example through the code. `i = 0`, `x = 2`, ..."
- "Now edge cases: empty input → ___; single element → ___; duplicates → ___; the largest value → ___."
- 发现 bug 时直接说："I see a bug here: ___. The fix is ___." 然后改。**这是加分项不是减分项。**

**⑥ 复杂度 + 追问（Complexity and follow-ups）**

- "Time is O(___) because each element is pushed and popped once. Space is O(___) for the map."
- "If the input were 1000 times larger... / if it were a stream... / if we needed this to be thread-safe..."（每道题的讲义里都有这类追问的答案要点。）

## 4. 「Logical and maintainable」长什么样（含可运行示例）

典型例子是一个 `BookFilter` 类：把"过滤"拆成独立的类/函数，用枚举规定参数，新增过滤条件不用改旧代码。好在把功能拆成独立的函数和类，而不是一整块实现；用类结构，新增过滤条件很容易。

同样的思想用 Python 写（一个面试里 5 分钟能写完的规模）。题意：给一个订单列表，支持多个可组合的过滤条件。

```python
from dataclasses import dataclass
from typing import Callable, Iterable, List


@dataclass(frozen=True)
class Order:
    order_id: str
    amount_cents: int          # money as integer cents, never float
    country: str


Predicate = Callable[[Order], bool]


def min_amount(cents: int) -> Predicate:
    return lambda order: order.amount_cents >= cents


def in_country(country: str) -> Predicate:
    return lambda order: order.country == country


def filter_orders(orders: Iterable[Order], *predicates: Predicate) -> List[Order]:
    """Keep orders that satisfy ALL predicates. With no predicates, keep everything."""
    return [o for o in orders if all(p(o) for p in predicates)]


ORDERS = [Order("a", 500, "US"), Order("b", 1500, "US"), Order("c", 2500, "DE")]
assert [o.order_id for o in filter_orders(ORDERS)] == ["a", "b", "c"]
assert [o.order_id for o in filter_orders(ORDERS, min_amount(1000))] == ["b", "c"]
assert [o.order_id for o in filter_orders(ORDERS, min_amount(1000), in_country("US"))] == ["b"]
assert filter_orders([], min_amount(1)) == []
```

为什么这样写是面试官想看的：
1. 每个过滤条件是一个小函数，名字说明意图（`min_amount`、`in_country`），**新增条件只加函数、不改旧代码**（对扩展开放，对修改关闭）。
2. 金额用整数分，不用浮点（金融场景的细节，资深面试官会注意）。
3. 边界在测试里写明：空输入、没有条件。**测试名字/用例对应业务含义**（测试名字应该描述业务和技术需求）。
4. 没有一行很炫但难懂的"技巧代码"——一团全是 one-liner 和技巧的代码很难优化、扩展和理解。

**把算法题写得 maintainable 的练习方法**：做完一题后，问自己「如果加一个新需求，我能不能只加代码不改旧代码？」例如把 LRU Cache 写成 `Node` 类 + `LRUCache` 类，再加「支持 TTL」；把 Two Sum 抽出 `find_pair(items, need_of)`（见第 01 讲模板）。

Python 具体建议：
- 用 `snake_case` 描述性命名；复杂数据用 `dataclass` 或 `NamedTuple`，不要到处 `x[0]`、`x[1]`。
- 辅助函数放在主函数里（闭包）或模块级，单一职责；一个函数不超过 ~20 行。
- 类型注解在面试里是加分项（尤其是接口），但不要为此拖慢速度。
- 标准库是朋友：`collections.deque / Counter / defaultdict`、`heapq`、`bisect`、`functools.lru_cache`；要说明你知道它们的复杂度。
- 不要把 `sorted(...)[...]` 之类的"便利写法"藏在 O(n) 的循环里却不说复杂度。

## 5. Senior 与 junior（passing）的区别

通过线和 senior 的差别如下，你要对标的是最后一列。

| 维度 | 通过线（junior / passing） | senior 的表现 |
|---|---|---|
| **澄清（谁在驱动对话）** | 等面试官解释清楚；被问才答 | **主动**驱动：先复述、问规模/输入分布/延迟 vs 吞吐、问「正确性的契约」（空输入、重复、非法输入返回什么）；说出假设并确认。把模糊的需求变成一页清晰的接口。 |
| **方案选择** | 想到一个能 work 的方案就写 | 先给 2–3 个方案及**取舍**（时间/空间/实现复杂度/可维护性/可扩展性），说出各自在哪种输入下会变差，然后给出推荐并请面试官确认。pick one and give a justification for it。 |
| **复杂度** | 能算出 O(·) | 能解释**为什么**（均摊、哈希冲突、退化树）、能说出常数和实际瓶颈（内存 vs CPU vs I/O），并知道理论下界。面试官常追问"So is it really O(1)?"。 |
| **代码质量** | 能运行；变量名勉强可读 | **生产级**：函数拆分、命名清楚、不变量写在注释或 assert 里、没有重复代码、错误输入有明确契约（抛什么/返回什么）、不用晦涩技巧。目标是 "easily maintainable, appropriately scalable, and extensible" 的代码。 |
| **测试** | 面试官问了才测 | **自己先**列测试矩阵（happy / edge / breaking / 大输入 / 性质），手动 trace 一遍，并说出如何自动化测试（表驱动 + 与暴力解随机对拍 + 并发压力测试）。run them through your code to verify your solution works。 |
| **追问** | 能答一两个；需要提示 | 预判追问并**主动**说：规模 ×1000 怎么办、流式输入、内存受限、并发 / 线程安全、API 设计、如何测试、如何监控（每道题的讲义里都有这些追问的答案要点）。 |
| **需求变化** | 推倒重来 | 在原代码上扩展（work with the solution you've already crafted, don't delete the whole thing）。 |
| **用提示** | "I'm stuck" | 说出已经尝试的方向和为什么不行，提出有方向的问题；把提示写下来并用上。 |
| **不过度设计** | 要么过于简单，要么堆模式 | Keep it simple, don't over-engineer。先 working，再按需求演进，只在有明确收益时引入抽象。 |

**senior 的一句话标准**：面试官离开房间时，能写出一条清楚的 hiring 理由——"这个人把问题的契约、方案取舍、实现质量、测试和扩展都自己带着走了，我基本没有给提示。"

## 6. 45 分钟时间线（一道主题题；两道题则各 20 分钟左右）

单场约 55–60 分钟，还要留时间给行为问题。下面的节奏假设你有约 45 分钟用于编码部分：

| 时间 | 做什么 | 检查点 |
|---|---|---|
| 0:00–0:05 | 复述题意 + 澄清（输入范围、空、重复、返回契约）+ 说假设 | 面试官点头了吗？ |
| 0:05–0:10 | 一个小例子手算；写 2–3 个边界用例（现在就列，之后拿来验证）；说暴力解及复杂度 | 瓶颈说出来了吗？ |
| 0:10–0:15 | 提出优化思路（对应的模式）、列取舍、选定并征得同意；口述一遍计划 | 有没有说为什么不用另一个？ |
| 0:15–0:30 | 编码：先主流程，再辅助函数；变量边写边说含义；不写伪代码 | 15 分钟还没写完核心 → 先写一个能跑的简单版本（先写一个能跑的版本） |
| 0:30–0:37 | **自己测试**：拿例子逐行 trace，再跑边界用例；发现 bug 就说出来改 | 不要等面试官问 |
| 0:37–0:40 | 复杂度总结（时间/空间 + 一句为什么） | |
| 0:40–0:45 | 追问环节：规模 ×1000 / 流式 / 内存 / 并发 / 接口 / 测试 | 用每题的「资深追问」答案要点；先说方向再说细节 |

**两道题的变体**：每道 ~20 分钟，压缩 ①–③ 到 6 分钟，编码 8 分钟，测试 4 分钟，追问 2 分钟；第一题做不出时，**先交付一个能跑的暴力解，说明瓶颈，再提出优化**，不要沉默。

**时间管理规则**：
- 10 分钟内必须开始写代码（但澄清不要省）。
- 卡住超过 2 分钟 → 说出你的思路并问一个有方向的问题。
- 剩 8 分钟：停止加功能，开始测试。

## 7. 面试当天清单

- [ ] 语言选 Python，并告诉面试官（"I'll use Python"）。
- [ ] 在线编辑器里没有编译器——写完自己读一遍：缩进、括号、变量名拼写、是否 `return`。
- [ ] 复杂度要说两件事：时间和空间，并且说 n 是什么。
- [ ] 每道题结束前说一句追问回答的**方向**（规模 / 流式 / 并发 / 测试），哪怕面试官没问。
- [ ] 卡住时保持说话：做过的尝试、排除的方案、下一步的想法。

## 8. 追问与行为问题

- 每讲的「资深追问」就是第 5 节「追问」一行的具体内容；每道参考解带随机对拍测试，对应第 5 节「测试」一行。
- 每场面试都夹带 Leadership Principles 问题，所以编码场次里也要为行为追问留出心理时间；LP 故事和系统设计、LLD 的准备在各自的页面。
