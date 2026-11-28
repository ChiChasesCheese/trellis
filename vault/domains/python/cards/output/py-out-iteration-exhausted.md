---
id: py-out-iteration-exhausted
node: output.iteration
type: qa
step: 1
---
## Q
**用完就空的生成器**｜读代码说输出

```python
g = (x * x for x in range(3))
print(list(g))
print(list(g))
print(sum(g))
r = range(3)
print(list(r), list(r))
```

输出什么？

## A
**输出。**

```
[0, 1, 4]
[]
0
[0, 1, 2] [0, 1, 2]
```

**为什么。**

- 生成器表达式（generator expression）本身就是迭代器（iterator）：它记着自己走到哪，第一次 `list(g)` 把它走完。
- 走完之后再迭代，立刻结束且不报错：得到空列表，`sum` 为 0。
- `range` 是可迭代对象（iterable），每次迭代都会产生新的迭代器，所以可以反复用。

**语言为什么这样设计。**

- 迭代器协议规定迭代器的 `__iter__` 返回自己，状态存在对象里，值不保存：这样生成器占用 O(1) 内存，代价是不能回放。
- Java 的 `Stream` 用第二次会抛 `IllegalStateException`，是明确报错；Python 静默变空，更容易埋 bug。

**怎么写才对。**

```python
vals = list(g)           # 需要多次用就先存下来
# 或者每次调用函数，重新造生成器
```

**面试里一句话。**

A generator is its own iterator, so once consumed it stays empty, whereas a range or list creates a fresh iterator every time.
