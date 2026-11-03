---
id: craft-closure-factory-policies-2-late-binding-in-loops
node: craft.idioms.closure-factory-policies
type: qa
step: 2
---
## Q
**闭包工厂做策略 · 循环里造闭包为什么全变成最后一个**｜写法

运营配了三档退款比例 `[100, 50, 0]`，你在 `for` 循环里为每档造一个 `lambda fare: fare * p // 100`，放进列表。调用后三个策略给出一样的结果。问题出在哪？应该怎么写才让每个策略记住自己的那一档？

## A
**要点。** 闭包捕获的是变量（name binding），不是创建那一刻的值。循环里的 `p` 只有一个，三个 lambda 共享它，调用时读到的是循环结束后的最终值。修法是让每个策略有自己的作用域：把创建放进一个工厂函数，每次调用产生新的 `p`。

```python
def make_all(percents):
    policies = []
    for p in percents:
        policies.append(lambda fare: fare * p // 100)     # 三个 lambda 共享同一个 p
    return policies

def make_one(p):                   # 每次调用都有自己的 p
    return lambda fare: fare * p // 100

bad = make_all([100, 50, 0])
good = [make_one(p) for p in [100, 50, 0]]
print([f(1000) for f in bad])
print([f(1000) for f in good])
```

实际输出：

```
[0, 0, 0]
[1000, 500, 0]
```

**为什么。** 用工厂函数而不是在 lambda 里写默认参数 `lambda fare, p=p: ...`：后者给策略多开了一个调用方可以误传的参数，策略签名就不再是 `fare -> int`。

**易错。** 列表推导式里同样会共享变量，只是推导式有自己的作用域，不会泄漏到外面，不等于每次迭代各有一份。凡是「循环中创建回调」的地方（定时任务、事件处理、策略表）都要这样检查。
