---
id: py-out-iteration-zip-map
node: output.iteration
type: qa
step: 4
---
## Q
**zip 吞元素与 map 的惰性**｜读代码说输出

```python
it = iter(range(5))
print(list(zip(it, "ab")))
print(next(it))
m = map(print, [1, 2])
print("made")
list(m)
```

输出什么？

## A
**输出。**

```
[(0, 'a'), (1, 'b')]
3
made
1
2
```

**为什么。**

- `zip` 每轮先从左边的 `it` 取一个，再从右边取；第三轮取了 `it` 的 2，但 `"ab"` 已经耗尽，`zip` 停下，这个 2 就被丢掉了，所以下一个是 3。
- `map` 创建时一个函数都不调用，只返回一个迭代器；`print("made")` 先输出，`list(m)` 逐个消费时才打印 1、2。

**语言为什么这样设计。**

- `zip` 在最短的输入处停止，且按从左到右取值，所以把较长或有副作用的迭代器放在右边；Python 3.10 加了 `zip(strict=True)`，长度不等时抛错。
- Python 2 的 `map` 立即返回列表，Python 3 改成惰性迭代器（PEP 3100），可以处理无限流，也省内存。

**怎么写才对。**

```python
list(zip(a, b, strict=True))       # 长度必须相等
for x in data: print(x)           # 要副作用就用 for，别用 map
```

**面试里一句话。**

zip stops at the shortest input after already pulling one item from the earlier iterators, and map does nothing until it is consumed.
