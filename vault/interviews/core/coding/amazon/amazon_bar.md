# Amazon 编码面试在评什么（The Amazon coding bar，按 senior 准备）

> 调研日期：2026-10-15。来源只用 Amazon 官方页面；论坛说法一律不当事实用。自己的推断标 `推断`。
> Chi 的指令（2026-10-15）：岗位挂的是 SDE I，但**准备内容永远对标 senior（SDE II/III）**。本文第 5 节专门讲 senior 与 junior 的区别。

## 1. 官方怎么说（原文要点）

**主来源：Amazon 官方 SDE 面试备考课程**（`amazon.jobs` 页面：<https://www.amazon.jobs/en/software-development-interview-prep>；页面内容实际嵌在 <https://duaa2xs5z3ldn.cloudfront.net/index.html>，2026-10-15 读取）。关键原文：

| 主题 | 官方原话（英文原文，摘要处标注） |
|---|---|
| 评什么 | "Your evaluation will include three areas of coding: data structures and algorithms, logical and maintainable, and problem-solving." |
| 三者要合在一起 | "...your response should consider all three as an integrated approach." |
| **Logical and maintainable** | "This competency measures your ability to write maintainable, readable, reusable, and understandable code." 面试在看你怎么"structure your methods and classes to ensure the logical separation of concerns is clear"，变量、方法、类怎么命名，才能让"future developers with no previous knowledge of the code"理解、演进、调试。 |
| 测试 | "Test names should describe business and technical requirements, and the test code should be consistent with the test names." |
| 写什么代码 | "Be prepared to write syntactically correct code, no pseudo code." "Be ready to write code in real-time on an online editor." |
| 需求与边界 | "Be prepared to gather qualifying requirements and translate into clean written code, checking edge cases." |
| 工作代码的标准 | "Think through test cases (both working and breaking), edge cases, boundary conditions, null/nil/none etc. Try and enumerate these cases before you begin coding... Be sure to also confirm test cases with your interviewer." |
| 先跑通再优化 | "Start small, solving one thing at a time, and iterate over your solution as you ask questions or the interviewer does more follow-ups." |
| 简单 | "start with a working solution, no matter how simple, and enhance it as you go." / "avoid a single function that does everything." |
| 命名与拆分 | "Make sure that your method, parameter, and variable names are clear & descriptive (e.g. don't just use "a" or "foo") and try to separate out functionality into discrete methods/functions with clear responsibilities." |
| 数据结构与算法 | "This competency measures your ability to choose the most efficient run-time solutions." "You'll also be expected to compare various approaches and explain why the one you selected was the right one." |
| 追问数据结构原理 | 官方示例对话：面试官追问 "what time complexity of insertion and lookup for the dictionary/map did you use", 再问 "how does it achieve that performance?"，再问 "So is it really O(1)?"。点评："The candidate demonstrates more than just rote memorization of the performance characteristics of the data structure." |
| 取舍 | "If you're comparing two data structures or algorithms that each have some drawback (very common!), pick one and give a justification for it." |
| 复杂度表达 | "Demonstrate a solid grasp of runtime and space complexity tradeoffs even if not perfectly accurate O(n) syntax." |
| 问题解决的时间分配 | 把时间分成三块："Uncovering requirements and considering evolution of the situation." / "Implementing a first pass of the design and covering all requirements." / "Enhancing the solution... seeking out more requirements to show how your solution evolves when requirements change." |
| 出声思考 | "Think out loud... We want to hear how you're transforming the solution!" ; "Explain your approach before coding, and vocalize your thought process as you proceed." |
| 澄清问题 | "Make sure you understand the problem and functional and not functional implications before you jump into code." "Test your ideas with examples and callout any assumptions you are making — ask the interviewer if they agree with them as you go." |
| 用测试验证 | "Identify test cases (happy and edge ones) and run them through your code to verify your solution works." |
| 提示 | "There are no trick questions or trick hints, everything will be useful. When the interviewer provides a hint, write it down." / "saying "I'm stuck" is very general..." 要问有方向的问题。 |
| 不要过度设计 | "Keep it simple. Try not to over-engineer the solution to solve for things it's not supposed to." |
| 语言 | "pick the coding language you are most comfortable with" （播客里两位 senior 工程师）；不看特定语言知识，看 "the underlying computer science fundamentals"。 |

**官方播客里的几条做法（同一课程，两位 senior SDE 的音频文字稿，2026-10-15）**（转述，不是逐字）：

- 在线的 Livecode 只是**协作文本编辑器，背后没有编译器**；语法重要，但漏一个分号不会被扣分，重点是开放沟通你的过程。
- 看到自己在**复制粘贴一串 if**，就该抽成函数。
- 面试官不是纯粹来评判的，是来帮你的；保持对话，听他们的想法。
- 练习时**测试失败就把代码全删了重写**，说明没有想清楚、结构也不够可扩展；面试里新增需求或发现反例时，应在原有解法上改，不要推倒重来。
- 面试官会"继续问到把需求推到扩展情形"（extension of the problem），不是只要第一个解。

**辅助来源（官方，2026-10-15）**

- Amazon 招聘团队的 SDE 面试建议：<https://www.aboutamazon.com/news/workplace/amazon-job-interview-software-development-engineer-recruiter-tips> —— "The most important thing a SDE does at Amazon is write scalable, robust, and well-tested code. These are the main evaluation criteria." / "Also, check for edge cases and validate that no bad input can slip through." / "during the interview process, you will be asked to write syntactically correct code."
- SDE III 备考页（senior 档的官方期望）：<https://www.amazon.jobs/content/en/how-we-hire/sde-iii-interview-prep> —— 编码目标列为 Efficiency / Reliability / Robustness / Portability / Maintainability / Readability；"Your solutions will be inventive, secure, easily maintainable, appropriately scalable, and extensible. You'll write software that's easy for others to contribute to."；loop 是五场 55 分钟。
- SDE II 备考页：<https://www.amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep>（"You'll also document your team's software, including how it's constructed, tested, operated, and secured"——说明 senior 被期望考虑测试与运维）。
- SDE 面试常考主题：<https://www.amazon.jobs/en/landing_pages/software-development-topics> —— 官方只列了 "Data structures" 与 "Algorithms" 等主题名，并说 "Your interviewers won't be evaluating your ability to memorize all of the details"。
- 流程（SDE 备考课程，同上主来源）：面试由 4–5 位软件开发同事进行，"Each conversation is approximately 60 minutes long"；示例日程里**每一场都是「2 个 Leadership Principles + 1 个技术」**，每位面试官只负责约 2–3 个 SDE 面试能力项；全程虚拟，使用 coding 和 whiteboarding 网页应用。（Chi 的 onsite 是线下，具体工具以招聘邮件为准——**未确认**。）

**未找到的东西**：官方没有公开「评分表的分值」或「通过线」；`amazon.jobs/en/landing_pages/software-development-interview-prep` 这个旧路径已返回 "page not available anymore"（2026-10-15 抓取），请以上面的新地址为准。

## 2. 把官方标准翻译成可执行动作

官方的 5 个编码"准则组"，各自对应你在面试里要做的具体动作：

| 官方准则 | 你要做的动作 | 在本 kit 哪里练 |
|---|---|---|
| Problem solving：Ask questions | 开场 2–3 分钟问输入范围、空输入、重复、返回什么；用一个例子复述题意 | 每讲「资深追问」里的「接口 / 边界契约」条 |
| Problem solving：Justify decisions | 先说暴力解及其复杂度，再说瓶颈，再说优化；至少给出一个备选方案和取舍 | 每讲第 1 节「从最笨的解法开始」 |
| DS&A：Optimization / Shortcomings / Justification | 说出你选的数据结构为什么，以及它**在什么输入上会变差**（哈希冲突、退化成链的树） | 每讲「复杂度」与「常见 bug」 |
| Logical & maintainable：Simple / Maintainable / Organize | 函数拆分、命名、不写一个什么都干的大函数；辅助函数有单一职责 | 本文第 4 节的示例 |
| Working code | 写完**自己手动跑一遍**例子 + 边界，而不是等面试官问 | 本文第 3 节、第 6 节 |

## 3. 边写边说（How to talk while coding）

官方要求 "think out loud"。下面是一套可以直接说出口的英文句型（你说的是英文，所以这一节用英文），按阶段分：

**① 复述 + 澄清（Restate and clarify，2–4 分钟）**

- "Let me restate the problem to make sure I understand: given ___, return ___."
- "A few clarifying questions: can the input be empty? Can there be duplicates or negatives? What should I return if there is no answer?"
- "Is the input sorted? How large can n get? That tells me whether O(n²) is acceptable."
- "I'll assume ___ unless you tell me otherwise."（官方："callout any assumptions you are making"）

**② 例子 + 暴力解（Examples and brute force，3–5 分钟）**

- "Let me walk through a small example: ___. The answer is ___ because ___."
- "The brute force is ___, which is O(___). It's slow because ___ is repeated for every ___."
- "To do better I need ___ in O(1) / O(log n)... that suggests a hash map / heap / two pointers."

**③ 选方案并取得同意（Pick and confirm，1–2 分钟）**

- "I see two options: A is ___ with O(___) time and O(___) space; B is ___ with ___. Given the constraints, I'll go with A because ___. Does that sound OK?"（官方："pick one and give a justification for it"）

**④ 编码（Coding）**

- "I'll start with the helper that ___, then the main loop."
- 写每个关键变量时说它的含义/不变量："`left` is the start of the window; the window is always valid."
- 卡住时："I'm weighing X against Y. X is simpler but ___; I think Y is right because ___."
- 需要的函数名/参数不记得：先说出来（"I don't remember the exact name, I'll call it `___`—is that OK?"，官方原话："call that out and ask the interviewer if you can make up a name and arguments"）。

**⑤ 自测（Test your own code，5 分钟，**不要等面试官**）**

- "Let me trace the example through the code. `i = 0`, `x = 2`, ..."
- "Now edge cases: empty input → ___; single element → ___; duplicates → ___; the largest value → ___."
- 发现 bug 时直接说："I see a bug here: ___. The fix is ___." 然后改。**这是加分项不是减分项。**

**⑥ 复杂度 + 追问（Complexity and follow-ups）**

- "Time is O(___) because each element is pushed and popped once. Space is O(___) for the map."
- "If the input were 1000 times larger... / if it were a stream... / if we needed this to be thread-safe..."（本 kit 的每道题都有这类追问的答案要点。）

## 4. 「Logical and maintainable」长什么样（含可运行示例）

官方示例是一个 `BookFilter` 类：把"过滤"拆成独立的类/函数，用枚举规定参数，新增过滤条件不用改旧代码。官方点评："Code shows breaking functionality into separate functions and classes rather than a monolithic implementation" / "A class structure makes the addition of new filters ... easy."

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

为什么这样写是官方想看的：
1. 每个过滤条件是一个小函数，名字说明意图（`min_amount`、`in_country`），**新增条件只加函数、不改旧代码**（对扩展开放，对修改关闭）。
2. 金额用整数分，不用浮点（金融场景的细节，资深面试官会注意）。
3. 边界在测试里写明：空输入、没有条件。**测试名字/用例对应业务含义**（官方："Test names should describe business and technical requirements"）。
4. 没有一行很炫但难懂的"技巧代码"——官方播客原话的意思是：一团全是 one-liner 和技巧的代码很难优化、扩展和理解。

**把算法题写得 maintainable 的练习方法**（来自官方播客的建议，转述）：做完一题后，问自己「如果加一个新需求，我能不能只加代码不改旧代码？」例如把 LRU Cache 写成 `Node` 类 + `LRUCache` 类，再加「支持 TTL」；把 Two Sum 抽出 `find_pair(items, need_of)`（见第 01 讲模板）。

Python 具体建议：
- 用 `snake_case` 描述性命名；复杂数据用 `dataclass` 或 `NamedTuple`，不要到处 `x[0]`、`x[1]`。
- 辅助函数放在主函数里（闭包）或模块级，单一职责；一个函数不超过 ~20 行。
- 类型注解在面试里是加分项（尤其是接口），但不要为此拖慢速度。
- 标准库是朋友：`collections.deque / Counter / defaultdict`、`heapq`、`bisect`、`functools.lru_cache`；要说明你知道它们的复杂度。
- 不要把 `sorted(...)[...]` 之类的"便利写法"藏在 O(n) 的循环里却不说复杂度。

## 5. Senior 与 junior（passing）的区别

下面是对官方准则的**推断性展开**（官方没有给出分值表，我们对照 SDE II/III 页的期望来写，标 `推断`）。Chi 要的是后面一列。

| 维度 | 通过线（junior / passing） | senior 的表现 `推断` |
|---|---|---|
| **澄清（谁在驱动对话）** | 等面试官解释清楚；被问才答 | **主动**驱动：先复述、问规模/输入分布/延迟 vs 吞吐、问「正确性的契约」（空输入、重复、非法输入返回什么）；说出假设并确认。把模糊的需求变成一页清晰的接口。 |
| **方案选择** | 想到一个能 work 的方案就写 | 先给 2–3 个方案及**取舍**（时间/空间/实现复杂度/可维护性/可扩展性），说出各自在哪种输入下会变差，然后给出推荐并请面试官确认。官方："pick one and give a justification for it"。 |
| **复杂度** | 能算出 O(·) | 能解释**为什么**（均摊、哈希冲突、退化树）、能说出常数和实际瓶颈（内存 vs CPU vs I/O），并知道理论下界。官方示例就是追问"So is it really O(1)?"。 |
| **代码质量** | 能运行；变量名勉强可读 | **生产级**：函数拆分、命名清楚、不变量写在注释或 assert 里、没有重复代码、错误输入有明确契约（抛什么/返回什么）、不用晦涩技巧。官方 SDE III 页：目标是 "easily maintainable, appropriately scalable, and extensible" 的代码。 |
| **测试** | 面试官问了才测 | **自己先**列测试矩阵（happy / edge / breaking / 大输入 / 性质），手动 trace 一遍，并说出如何自动化测试（表驱动 + 与暴力解随机对拍 + 并发压力测试）。官方："run them through your code to verify your solution works"。 |
| **追问** | 能答一两个；需要提示 | 预判追问并**主动**说：规模 ×1000 怎么办、流式输入、内存受限、并发 / 线程安全、API 设计、如何测试、如何监控（本 kit 每道题都有这些追问的答案要点）。 |
| **需求变化** | 推倒重来 | 在原代码上扩展（官方播客："working with the solution that you've already crafted and not just deleting the whole thing"）。 |
| **用提示** | "I'm stuck" | 说出已经尝试的方向和为什么不行，提出有方向的问题；把提示写下来并用上。 |
| **不过度设计** | 要么过于简单，要么堆模式 | 官方："Keep it simple. Try not to over-engineer"。先 working，再按需求演进，只在有明确收益时引入抽象。 |

**senior 的一句话标准 `推断`**：面试官离开房间时，能写出一条清楚的 hiring 理由——"这个人把问题的契约、方案取舍、实现质量、测试和扩展都自己带着走了，我基本没有给提示。"

## 6. 45 分钟时间线（一道主题题；两道题则各 20 分钟左右）

官方没有规定每道题多长（loop 的单场约 55–60 分钟；每场还有 LP 问题，见第 1 节）。下面的节奏是 `推断`，假设你有约 45 分钟用于编码部分：

| 时间 | 做什么 | 检查点 |
|---|---|---|
| 0:00–0:05 | 复述题意 + 澄清（输入范围、空、重复、返回契约）+ 说假设 | 面试官点头了吗？ |
| 0:05–0:10 | 一个小例子手算；写 2–3 个边界用例（现在就列，之后拿来验证）；说暴力解及复杂度 | 瓶颈说出来了吗？ |
| 0:10–0:15 | 提出优化思路（对应的模式）、列取舍、选定并征得同意；口述一遍计划 | 有没有说为什么不用另一个？ |
| 0:15–0:30 | 编码：先主流程，再辅助函数；变量边写边说含义；不写伪代码 | 15 分钟还没写完核心 → 先写一个能跑的简单版本（官方："start with a working solution"） |
| 0:30–0:37 | **自己测试**：拿例子逐行 trace，再跑边界用例；发现 bug 就说出来改 | 不要等面试官问 |
| 0:37–0:40 | 复杂度总结（时间/空间 + 一句为什么） | |
| 0:40–0:45 | 追问环节：规模 ×1000 / 流式 / 内存 / 并发 / 接口 / 测试 | 用本 kit 每题的「资深追问」答案要点；先说方向再说细节 |

**两道题的变体** `推断`：每道 ~20 分钟，压缩 ①–③ 到 6 分钟，编码 8 分钟，测试 4 分钟，追问 2 分钟；第一题做不出时，**先交付一个能跑的暴力解，说明瓶颈，再提出优化**，不要沉默。

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

## 8. 与本 kit 其他部分的关系

- 每讲的「资深追问」是第 5 节「追问」一行的具体内容。
- 每道题的参考解（`solutions/`）带随机对拍测试，对应第 5 节「测试」一行。
- LP（Leadership Principles）故事在 `../lp/`，系统设计在 `../sd/`，LLD 在 `../lld/`（各自的 kit 部分）；官方示例日程里每场都有 LP，所以编码场次里也要为 LP 追问留出心理时间。
