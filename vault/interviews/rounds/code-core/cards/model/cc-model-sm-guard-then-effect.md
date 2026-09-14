---
id: cc-model-sm-guard-then-effect
node: model.state-machine
type: qa
---
## Q
Write the shape of a command handler in a machine where invalid commands are silently ignored.

## A
**Guard fully, then act — never interleave.**

```python
def succeed(pid):
    p = payments.get(pid)
    if p is None or p.state != "PROCESSING":
        return                       # all guards first
    p.state = "COMPLETED"            # then all effects
    balances[p.merchant] += p.amount
```

Interleaving produces the worst bug class in these problems: a command that is rejected halfway, leaving the state advanced but the money not moved. It is invisible in the output of the part that introduced it and surfaces two parts later.

The same shape makes the handler testable — the guard block is the list of ignore-path tests. See [[cc-input-mal-validate-before-mutate]].

## Q zh
在"无效命令被静默忽略"的状态机里，写出命令处理函数的形状。

## A zh
**先完整守卫，再执行 —— 绝不交错。**

```python
def succeed(pid):
    p = payments.get(pid)
    if p is None or p.state != "PROCESSING":
        return                       # all guards first
    p.state = "COMPLETED"            # then all effects
    balances[p.merchant] += p.amount
```

交错会产生这类题里最糟的一种 bug：命令在半路被拒，状态却已经推进、钱却没动。它在引入它的那一部分的输出里看不见，两部分之后才浮现。

同样的形状也让处理函数可测试 —— 守卫块就是"忽略路径"测试清单。见 [[cc-input-mal-validate-before-mutate]]。
