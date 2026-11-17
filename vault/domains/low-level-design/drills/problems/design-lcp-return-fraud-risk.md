---
nodes: [lcproject.lcp-return-fraud-risk, errors.boundary-validation, data.defensive-copy, quality.testability, ai.decomposition]
tags: [problem]
---
# Drill：退货风险评分修复（Return Risk Assessment）

一个退货评分引擎根据星级评分、订单金额（分）和账龄（天）给出通过、人工复核或拒绝，另有批量入口。现有代码能跑，但在校验、评分表、阈值边界、决定和批量的错误码上有错，同样条件的请求在边界上得到前后不一致的决定。规模是一个文件、几十行；难点是五处缺陷互相叠加，只看最后的结果分不清哪处错了。

**分关要求**（每关做完再看下一关，像真实的修复轮）
- 第 1 关（约 10 分钟）：先不改代码，把规则逐条对照现有代码，写出差异清单；再修校验：入参必须恰好是 `int`，评分 1 到 5，金额与账龄不小于 0，`True` 也无效，错误是 `ServiceError(400, "invalid_input")` 且发生在计算之前。每处先写一个会失败的测试。起始代码已经做对的（`True`、字符串、`None` 被拒绝，金额 10000 得 15，账龄两个阈值，总分 30 进复核）要保住，写测试钉住它们，别让修复把它们改坏。
- 第 2 关（约 10 分钟）：修三个分项：评分用表 40、30、20、10、0；金额 10000 与 50000、账龄 30 与 180 的下界都含。每个下界写两个测试：恰好下界和前一格。
- 第 3 关（约 10 分钟）：修总分与决定：总分 30 是人工复核、60 是拒绝。测决定边界时选金额与账龄都不压边界的输入，想清楚为什么。
- 第 4 关（选做，约 15 分钟）：修批量：坏记录的 `error` 是 "invalid_input"、保序、只遍历一次、上游迭代器的异常原样抛出；返回的嵌套字典每次新建、不修改传入的记录。最后写三个书面回答：阈值测试怎么选、策略版本怎么保留解释、指标怎么区分无效输入与策略拒绝。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-return-fraud-risk/starter.py` 当作要修的服务，改完后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-return-fraud-risk -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给规则和两个数字例子，要求它先列出代码与规则的差异、不改代码；你核对清单后，一次只让它修一类缺陷、只给它一个失败的测试，改完立刻运行测试。边界归属、`bool` 是否有效、迭代器异常是否吞掉、返回值是否共享这些决定自己留着；期望值自己独立算出，不接受“把测试改成通过”。

**评分点**
- 写得出开工前的合同：校验先于计算、每个下界都含、总分原样相加、批量规则、无状态（[[lcp-return-fraud-risk-contract-rules]]、[[lcp-return-fraud-risk-state-and-invariant]]）。
- 知道 `bool` 是 `int` 的子类，类型检查在范围比较之前（[[lcp-return-fraud-risk-contract-rules]]）。
- 阈值用有序表加二分，每个下界测两侧，总分边界用不压边界的输入（[[lcp-return-fraud-risk-contract-rules]]、[[lcp-return-fraud-risk-reflection-threshold-tests]]）。
- 批量里 `try` 只包一条记录，上游异常照常抛出，输入只遍历一次（[[lcp-return-fraud-risk-contract-rules]]）。
- 返回值每次现建，不共享可变对象（[[lcp-return-fraud-risk-contract-rules]]）。
- 能指出代码里的五处缺陷（评分 0 放行、评分公式、金额 50000、总分 60、批量错误码）并给出能抓住它们的测试，也说得出哪些已经是对的（[[lcp-return-fraud-risk-contract-rules]]）。
- 能指挥智能体：规则先行、先列差异、一次一类缺陷（[[lcp-return-fraud-risk-contract-rules]]）。
- 能回答策略版本化与指标区分（[[lcp-return-fraud-risk-reflection-policy-versioning]]、[[lcp-return-fraud-risk-reflection-invalid-vs-reject]]）。

**题解**：[[solution-lcp-return-fraud-risk]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
