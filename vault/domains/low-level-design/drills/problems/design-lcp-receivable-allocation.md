---
nodes: [lcproject.lcp-receivable-allocation, oop.values, errors.boundary-validation, fluency.time-numbers, data.invariants]
tags: [problem]
---
# Drill：交易汇总与应收分账（Aggregate Transactions）

一个支付结算系统每天把卡交易汇总成应收款，再把每笔应收款按合约切成几份：固定额或按基点的百分比，余下的归商户。输入各最多一万条，金额最多 10 亿分。规模是一个文件、一百多行；难点全在数字与出行规则：百分比读哪个金额、取整往哪边、零要不要输出、钱不够时谁先拿，每一处都有一个隐藏测试会去踩的边界。

**分关要求**（每关做完再看下一关，像真实的实现轮）
- 第 1 关（约 10 分钟）：写 `register_receivables`：按 (商户, 卡类型, 付款日) 汇总，客户编号不参与，重复行各算一次，空输入返回空列表。先把两个汇总例子写成测试。
- 第 2 关（约 15 分钟）：写 `allocate_receivables` 的固定额主干：每笔应收款一个"剩余"，合约按输入顺序领钱，拿到正数才出合约行，商户行一定出（余额为零也出），键不在应收款里的合约被忽略。
- 第 3 关（约 15 分钟）：加百分比合约：`原始金额 * 基点 // 10000`，向下取整，永远读原始金额。为"固定 400 之后的 25% 是 250 不是 150"和"50 分的 58% 是 29"各写一个测试，先看它们红。
- 第 4 关（选做，约 10 分钟）：合约先按键归组让一万 × 一万不变慢；加守恒检查和对重复键、负请求的拒绝；写"调用前后比较输入"的测试；再写两个书面回答：分组键、合约顺序与原始金额怎样决定结果，结果怎样与输入脱钩。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-receivable-allocation/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --no-project --python 3.11 --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-receivable-allocation -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给规则和 README 里的三个数字例子（350 的汇总、400 加 25% 得 250 和 351、再加固定 500 得 351 和零余额），一次只让它实现一个函数，一次只给它一个失败的测试，改完立刻运行测试。取整方向、百分比的基数、零行要不要出这三处语义自己定，不交给它顺手选；让它另写一个用 `Fraction` 的模拟实现，在随机数据上和解答比较，期望值自己独立写出，不接受"把测试改成通过"。

**评分点**
- 写得出开工前的合同：三元组分组、百分比按原始金额向下取整、先到先得、合约行拿到正数才出而商户行一行不少（[[lcp-receivable-allocation-contract-rules]]）。
- 说得清为什么每笔钱要有 `original` 和 `remaining` 两个数，守恒与负请求为什么用异常守，合约为什么先按键归组（[[lcp-receivable-allocation-state-and-invariant]]）。
- 知道固定 400 之后的 25% 按原始金额是 250、按剩余是 150，并且用整数做除法而不是浮点数或 `round()`（[[lcp-receivable-allocation-reflection-original-vs-remaining]]）。
- 说得出结果与输入脱钩靠冻结记录、新建列表和无状态函数，写得出能抓到原地排序和缓存的测试（[[lcp-receivable-allocation-reflection-detached-and-verified]]）。
- 写得出能抓住缺陷的测试：零余额的商户行、零值合约不出行、键大小写、钱分完后后面的合约（[[lcp-receivable-allocation-contract-rules]]、[[lcp-receivable-allocation-reflection-original-vs-remaining]]）。

**题解**：[[solution-lcp-receivable-allocation]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
