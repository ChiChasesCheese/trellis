---
id: cc-python-pitfalls-late-binding-closures
node: python.pitfalls
type: qa
---
## Q
`fns = [lambda: i for i in range(3)]` then `[f() for f in fns]` gives `[2, 2, 2]`. Why, and what are the two fixes?

## A
**Closures capture the variable, not its value.** All three lambdas refer to the same `i`, which is `2` once the loop has finished.

```python
fns = [lambda i=i: i for i in range(3)]              # bind at definition
fns = [functools.partial(op, i) for i in range(3)]   # bind by argument
```

- It appears wherever you build functions in a loop: per-rule predicates, per-column `key=` functions, a table of handlers.
- The symptom is characteristic — every handler behaves like the **last** one, so only the final test case passes and the failure looks like a logic bug.

## Q zh
`fns = [lambda: i for i in range(3)]`，然后 `[f() for f in fns]` 得到 `[2, 2, 2]`。为什么？两种修法是什么？

## A zh
**闭包捕获的是变量，不是它的值。** 三个 lambda 引用的是同一个 `i`，而循环结束后它是 `2`。

```python
fns = [lambda i=i: i for i in range(3)]              # 在定义处绑定
fns = [functools.partial(op, i) for i in range(3)]   # 通过参数绑定
```

- 只要你在循环里造函数它就会出现：逐规则的谓词、逐列的 `key=` 函数、一张 handler 表。
- 症状很典型 —— 每个 handler 都表现得像**最后**那个，于是只有最后一个测试用例通过，故障看起来像逻辑 bug。
