---
id: testing-partitioning-white-box
node: testing.partitioning
type: qa
step: 3
---
## Q
按规格（黑盒）设计完用例后，读代码（白盒）还能补出哪些用例？下面这个函数，规格只说「超过上限就截断，除非 strict 为真时报错」，你会补哪些用例？

```python
def fit(tokens, limit, strict=False):
    if len(tokens) > limit and not strict:
        return tokens[:limit]
    if len(tokens) > limit:
        raise ValueError("too long")
    return tokens
```

## A
**白盒补用例的方法：把代码里的每个条件拆开，让每个判断的真和假都至少被走到一次，并让组合条件里的每个子条件都能单独决定结果。**

- **从分支看：** 第一个 `if` 有真、假两条路，第二个 `if` 也有。要走遍四条路：短输入（两个 `if` 都为假）、超长且非 strict（第一个为真）、超长且 strict（第一个为假、第二个为真）。
- **从组合条件看：** `len(tokens) > limit and not strict` 有两个子条件，要有用例证明各自能改变结果：
  - 超长、非 strict → 截断；
  - 超长、strict → 不截断（转到报错）：证明 `strict` 起作用；
  - 等长、非 strict → 不截断：证明长度条件起作用。
- **从边界看代码里的比较：** 代码写的是 `>`，所以 `len == limit` 必须原样返回，`len == limit + 1` 必须截断或报错。
- **从代码暴露的隐含输入看：** `limit = 0`（返回空列表）、`limit` 为负数（`tokens[:-1]` 会悄悄去掉最后一个元素，这是规格没说的 bug）、空 `tokens`。
- **补出的用例：** `(len 3, limit 5)`、`(len 5, limit 5)`、`(len 6, limit 5, strict=False)`、`(len 6, limit 5, strict=True)`、`(limit 0)`、`(limit -1)`。最后一个很可能揭出一个真 bug：负数上限应当被拒绝。
- **工具辅助：** `pytest --cov --cov-branch` 会列出没有走过的分支，告诉你还缺哪条路；但它不会告诉你 `limit` 为负这种「代码根本没处理」的情况，那要靠读代码时问「这个值可能是什么」。
