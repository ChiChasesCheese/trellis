---
id: craft-recursive-descent-parsing-5-across-problems-and-scales
node: craft.patterns.recursive-descent-parsing
type: qa
step: 5
---
## Q
**递归下降解析 · 计算器、公式、WHERE 条件、迷你 SQL 里的同一个骨架**｜模式

Basic Calculator III、电子表格公式、查询条件解析器、迷你 SQL，输入和输出都不一样。它们共享什么骨架？LeetCode 的标准解为什么用显式栈，而 LLD 里却用递归？

## A
**要点。** 同一个流水线：分词（正则）→ 递归下降解析 → 不可变语法树 → 求值/匹配。优先级决定方法的层数，语言不同只是层数和叶子不同。

```python
# spreadsheet-engine：数字运算，叶子是数字/引用/函数
"""递归下降：expr 管 + -，term 管 * /，unary 管负号，atom 管数字、引用、括号、函数。"""

# query-condition-parser：布尔运算，叶子是 field op literal
or_expr  := and_expr (OR and_expr)*
and_expr := not_expr (AND not_expr)*
not_expr := NOT not_expr | primary
```

**见于。** basic-calculator-iii、spreadsheet-engine、query-condition-parser、amz-in-memory-db。

**不变的。** 优先级 = 调用层次，括号 = 回到最低层，同级用循环，顶层检查吃完。**变化的。** 叶子（数字 vs 比较谓词），节点的求值（算术 vs 三值逻辑），以及错误类型。

**递归 vs 显式栈。** 每层括号要经过 `expr → term → unary → atom` 四个 Python 调用，默认递归上限是 1000，所以大约 250 层括号就会触顶（`RecursionError`）。LeetCode 版括号可嵌套几千层，所以标准解用显式栈（遇 `(` 把当前层压栈），代价是把优先级写成「项列表」的技巧，不能直接扩展到更多运算符。LLD 的公式和 WHERE 条件是人写的，嵌套很浅，递归下降最容易扩展、最容易读。选择依据是输入的规模是否由对手控制。

**信号。** 需求里出现「条件表达式」「公式」「过滤规则」「括号」「AND/OR 优先级」；或者你想用 `split` 或 `eval` 来处理一段用户写的文本。

**尺度对照。** 力扣：一遍扫描的栈解法。低层设计：递归下降 + 冻结的语法树，解析与存储互不知道对方。分布式：规则引擎、SQL 解析器、配置 DSL，都是词法 → 语法 → 语义三层。变化：用户输入来自网络时，嵌套深度、token 数要设上限（否则一条恶意的几万层括号就能让服务递归崩溃），语法树可以缓存（同一条规则解析一次、按行复用）。
