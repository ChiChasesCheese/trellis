---
nodes: [lcproject.lcp-payment-form-validation, fsm.guards-actions, errors.boundary-validation]
tags: [problem]
---
# Drill：支付表单校验（Payment Form Validation）

一个支付页面有卡号、姓名、月份、年份、CVV 五个输入框。你要写页面背后的校验组件：保存每个框里的原始字符串，知道哪些框被碰过，
判断每个框是否有效，只在"碰过且无效"时给出固定错误文字，并告诉页面能不能提交。年份窗口由外面注入的当前年份决定，调用都是顺序的。计划用时 45 分钟。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读合同，把 `starter.py` 文档字符串里的规则逐条改写成自己的断言。只做 `change` 和格式判断：
  十六位卡号、纯英文字母姓名、`01` 到 `12` 的月份、`currentYear` 起四年的年份、三位 CVV。无效输入自己列一张表：空串、差一位、前后空白、末尾换行、正负号、全角数字、阿拉伯数字、带重音的字母。
- 第 2 关（约 15 分钟）：`blur`、`error`、`canSubmit`。改值不碰触碰；未碰的无效字段没有错误；碰过的有效字段没有错误；
  五个字段各让一次"只有它没失焦"和"只有它无效"，`canSubmit` 都应为假；把 CVV 改短，`canSubmit` 立刻为假。
- 第 3 关（约 10 分钟）：`reset` 与快照隔离。重置保留年份；旧快照在之后的任何操作下不变；改返回的快照不影响表单；两个表单互不影响。
- 第 4 关（选做，约 15 分钟）：`apply_action` 把页面发来的 JSON 体变成一次操作，形状不对就在碰表单之前拒绝；再加 `touch_all` 与 `first_invalid`。
  最后写两篇各约一百五十字的短文：有效性、触碰、可见错误怎么区分；怎样不依赖默认年份检查重置与快照隔离。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-payment-form-validation/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-payment-form-validation -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把规则和一个数字例子交给它，
一次只给它一个失败的测试，先写规则表和格式判断，再写 `blur` 和快照。"条目里存什么"这个设计决定自己留着，写进给它的指令。
每次改动之后先跑全部测试，再读 diff：看它有没有把 `valid` 存进条目、有没有在 `change` 里 `strip()` 或标触碰、
有没有用 `int()` 或 `\d` 判断数字、有没有把内部字典直接放进快照、有没有改测试。最后自己写隔离测试，不要让它代写。

**评分点**
- 开工前把合同定成规则：改值不碰触碰、错误要"碰过且无效"、提交要"全有效且全碰过"、重置保留年份（[[lcp-payment-form-validation-contract-rules]]）。
- 口径说得清：数字只认 ASCII，年份窗口含两端，月份与年份互相独立，前导零保留（[[lcp-payment-form-validation-contract-rules]]）。
- 说得出要保存的状态与最要紧的不变量：只存字符串和触碰标记，其余现算（[[lcp-payment-form-validation-state-and-invariant]]）。
- 能讲清用户敲到一半跳走再回来时 `valid`、`touched`、`error` 各怎么变（[[lcp-payment-form-validation-reflection-error-visibility]]）。
- 重置与快照隔离的检查不依赖默认年份：两个注入年份、持有旧快照、破坏返回值、两个表单（[[lcp-payment-form-validation-reflection-reset-and-snapshot]]）。
- 给编程智能体的第一条指令带着规则和数字例子，一次一个失败用例，状态设计自己留着（[[lcp-payment-form-validation-contract-rules]]）。

**题解**：[[solution-lcp-payment-form-validation]]——先做，再看。同样用"名字到函数的表"、严格输入约定的相邻项目见 [[solution-lcp-feature-flag]]。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
