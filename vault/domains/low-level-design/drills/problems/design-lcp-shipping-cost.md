---
nodes: [lcproject.lcp-shipping-cost, errors.boundary-validation, oop.values, data.invariants, data.defensive-copy, fluency.time-numbers]
tags: [problem]
---
# Drill：运费计算（Shipping Cost）

一个电商的运费服务按"目的国加商品"保存分段费率：每一段要么按件收（`incremental`），要么进入就一次性收一笔（`fixed`）。服务要整批登记费率、按订单逐段累计报价、列出现有费率。规模是一个文件、一百五十行左右；难点在输入语法、分段表的连续性、整批原子，以及报价的五层错误顺序，每一处都有隐藏测试会去踩的边界。

**分关要求**（每关做完再看下一关，像真实的实现轮）
- 第 1 关（约 20 分钟）：写 `register_rules`：六段语法、ASCII 数字与前导零、每个数字 ≤ 1,000,000、语法先于分段；按（国家，商品）排序后从 1 起首尾相接、末段无上界；整批原子、按对替换。先把"缺口、重叠、零锚点、末段有限、最大小于最小"各写成一个测试，再实现。
- 第 2 关（约 15 分钟）：写 `calculate_shipping`：五层错误顺序、同商品先合并、逐段累计、数量 0 拒绝、金额两处上界检查、`breakdown` 按商品名 ASCII 排序。为"合并前后固定段收费不同"和"每个商品都合规、合起来超限"各写一个测试。
- 第 3 关（约 15 分钟）：写 `list_rules`：排序键、行的形状、过滤只做完全相等、没有匹配也不创造国家；再检查返回值与输入、内部状态互相独立。
- 第 4 关（选做，约 10 分钟）：写三个书面回答：先验证整批再赋值与隔离；合并先于算价，用行数、商品数、分段数分析成本；费率持久化、多实例、费率会变时，怎样让一次报价读同一个版本。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-shipping-cost/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --no-project --python 3.11 --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-shipping-cost -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给规则和数字例子（水壶三段、`kettle,6` 加 `kettle,5` 合并成 2400、一批含缺口的坏批次），一次只让它实现一个方法，一次只给它一个失败的测试，改完立刻运行测试。语法与分段的先后、"最小是 0"算哪一层、商品名畸形算 400 还是 404、替换而不是合并，这些语义决定自己留着；让它另写一个"一件一件地买"的对照实现，在随机分段表上和解答比较；期望值自己独立写出，不接受"把测试改成通过"。

**评分点**
- 写得出开工前的合同：语法先于分段、分段表连续、整批原子按对替换、报价五层错误、先合并再逐段累计、输入严格（[[lcp-shipping-cost-contract-rules]]）。
- 说得清服务要存什么、分段表为什么只能由 `build` 构造，以及"副本上建表、成功后一次赋值"这条不变量（[[lcp-shipping-cost-state-and-invariant]]）。
- 知道坏批次靠"先验证后赋值"不留痕，返回值靠冻结的内部值和新建的容器隔离，并说得出两个并发登记为什么会丢一批（[[lcp-shipping-cost-reflection-atomic-and-detached]]）。
- 知道固定段必须在合并之后才算、整体复杂度 `O(L + P·T + P log P)`，能提出累计前缀加二分的优化，并说出费率版本化的做法（[[lcp-shipping-cost-reflection-merge-before-pricing]]）。
- 写得出能抓住缺陷的测试：同批含合法商品的缺口批次、语法错在批次末尾、"最大小于最小"、恰好等于上界与多一分、超长的零串（[[lcp-shipping-cost-contract-rules]]、[[lcp-shipping-cost-state-and-invariant]]）。

**题解**：[[solution-lcp-shipping-cost]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
