---
id: pl-functional-iterators-laziness-foundation-python-iterator-protocol
node: functional.iterators-laziness
type: qa
step: 2
---
## Q
Python 的迭代器协议是什么？可迭代对象和迭代器有什么区别，生成器表达式为什么用完就空了？

## A
Python 的 `for x in obj` 被翻译成：

1. 调用 `iter(obj)`，也就是 `obj.__iter__()`，得到一个**迭代器**；
2. 反复调用 `next(it)`，也就是 `it.__next__()`，直到抛出 `StopIteration` 为止。

两个角色：**可迭代对象**（iterable，有 `__iter__`，如 `list`、`dict`、文件）每次 `iter()` 都给你一个新的迭代器，可以重复遍历；**迭代器**（iterator，有 `__next__`，且 `__iter__` 返回自己）是一次性的游标，遍历过的元素不会重来。

```python
g = (x * x for x in range(4))     # 生成器表达式：惰性，是迭代器
sum(g), sum(g)                    # (14, 0)：第二次什么都没有
```

惰性同样适用于 `map` 和 `filter`（在 Python 3 里返回迭代器）：

```python
nums = map(lambda x: print("side effect", x) or x, [1, 2])
print("nothing yet")        # 先打印这个
list(nums)                  # 这时才打印两行 side effect
```

列表推导式 `[x*x for x in ...]` 则是**立即**求值，一次性造出完整的列表；换成圆括号 `(x*x for x in ...)` 就变成惰性的生成器表达式。

协议这么简单（两个方法加一个异常），是 Python 鸭子类型的典型：任何对象只要有这两个方法，就能被 `for`、`sum`、`list()`、`zip()` 使用。
