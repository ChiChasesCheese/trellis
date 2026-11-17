---
nodes: [lcproject.lcp-currency-conversion, errors.boundary-validation, data.defensive-copy, fluency.time-numbers, parsing-io.regex]
tags: [problem]
---
# Drill：汇率换算（Currency Conversion）

一个支付服务收到有向汇率报价，要回答三类问题：直达汇率、至多经过一种中转货币的全部汇率、所有简单路径里的最优汇率。货币至多 8 种，报价以 `FROM:TO:RATE,…` 的文本批量登记，整批要么全生效、要么全不生效。规模是一个文件、一百多行；难点在输入语法、浮点容差与平局规则、错误优先级，每一处都有一个隐藏测试会去踩的边界。

**分关要求**（每关做完再看下一关，像真实的实现轮）
- 第 1 关（约 15 分钟）：写 `register_rates` 和 `get_direct_rate`：非空字符串、三段记录、货币码 3–5 位大写、汇率语法与 [1e-12, 1e12]、至多 8 种货币、后写覆盖、整批原子。先把 14 条规则里的每个数字例子写成测试，再实现。
- 第 2 关（约 15 分钟）：写 `get_single_hop_rates` 和 `list_pairs`，补上查询的错误优先级（格式 400、未出现 404、无路线 404）、两个码相同的结果、只作终点的货币；返回值每次新建。
- 第 3 关（约 20 分钟）：写 `get_best_rate`：递归枚举简单路径，乘积从 1 起从左到右连乘，以全局最大值 M 为基准的 1e-5 容差，先边数、再货币序列字典序。为"返回的乘积略小于 M"和"基准不能是已选路径"各写一个测试。
- 第 4 关（选做，约 15 分钟）：写三个书面回答：坏批次与返回值怎样不留痕、顺序调用与并发的区别；简单路径、八种货币的成本与容差；规模变大或接实时行情时改哪一处、语义怎么取舍。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-currency-conversion/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --no-project --python 3.11 --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-currency-conversion -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给规则和 README 里的数字例子（`SGD:HKD:5.8,HKD:NOK:1.3,SGD:NOK:7.1` 的三个查询、一批含坏记录的登记），一次只让它实现一个方法，一次只给它一个失败的测试，改完立刻运行测试。容差基准、平局顺序、错误优先级这些语义决定自己留着；让它另写一个"子集排列穷举"的对照实现，在随机图上和解答对拍；期望值自己独立写出，不接受"把测试改成通过"。

**评分点**
- 写得出开工前的合同：整批原子、严格输入、有方向与后写覆盖、错误先格式后货币后路线、最优路线的选择规则、返回快照（[[lcp-currency-conversion-contract-rules]]）。
- 说得清服务要存什么、货币集合为什么由边推出，以及"簿子不可变、成功后一次赋值"这条不变量（[[lcp-currency-conversion-state-and-invariant]]）。
- 知道坏批次靠"先解析后赋值"不留痕，返回值靠新建容器隔离，并说得出两个并发登记为什么会丢一批（[[lcp-currency-conversion-reflection-atomic-and-snapshots]]）。
- 知道简单路径让环走不起来、八种货币只有 1957 条路径，容差以全局最大值为基准，返回被选路径自己的乘积（[[lcp-currency-conversion-reflection-routes-and-tolerance]]）。
- 写得出能抓住缺陷的测试：容差恰好等于 1e-5、基准漂移、汇率边界两侧、同批更早的覆盖不泄漏（[[lcp-currency-conversion-contract-rules]]、[[lcp-currency-conversion-reflection-routes-and-tolerance]]）。

**题解**：[[solution-lcp-currency-conversion]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
