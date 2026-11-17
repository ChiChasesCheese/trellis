---
id: fluency-iteration-any-all-comprehension
node: fluency.iteration
type: qa
step: 2
---
## Q
判断“有没有负数”写成 `any([x < 0 for x in xs])`，和 `any(x < 0 for x in xs)` 差在哪？推导式、`any/all`、普通 `for` 循环各适合什么，什么时候该退回循环？

## A
**一个结果用推导式或生成器，带副作用就写循环**

- **方括号先建完整个列表**：`any([...])` 对每个元素都求值，才交给 `any`；去掉方括号是生成器表达式，`any` 遇到第一个真值就停止，后面的元素不再求值；
- **`all` 和 `any` 的空值**：`all([])` 为 `True`，`any([])` 为 `False`；“所有订单都已支付”对空订单列表为真，业务上是否合理要单独判断；
- **计数**：`sum(1 for x in xs if x > 1)` 或 `sum(x > 1 for x in xs)`（`bool` 是 `int`）；
- **推导式适合“由一个序列算出另一个”**：一层循环、至多一个 `if`；嵌套超过两层、要在里面 `try`、要累计多个结果、要写日志，就改回普通 `for`；
- **不要为了副作用写推导式**：`[print(x) for x in xs]` 建了一个无用的列表；
- **可读性是标准**：一行放不下就拆开，推导式写成三行比挤成一行的嵌套更好读。

```python
calls = []
def neg(x):
    calls.append(x)
    return x < 0

print(any(neg(x) for x in [5, -1, 7, -2]), calls)    # True [5, -1]：遇真即停
calls.clear()
print(any([neg(x) for x in [5, -1, 7, -2]]), calls)  # True [5, -1, 7, -2]：全算了
print(all([]), any([]))                              # True False
print(sum(x > 1 for x in [1, 2, 3]))                 # 2
```

**知识点：**迭代写法（Iteration Style）
