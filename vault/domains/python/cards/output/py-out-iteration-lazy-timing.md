---
id: py-out-iteration-lazy-timing
node: output.iteration
type: qa
step: 2
---
## Q
**生成器何时读数据**｜读代码说输出

```python
xs = [1, 2, 3]
g = (x for x in xs)
xs.append(4)
xs = [9]
print(list(g))
ys = [1, 2]
g2 = (x + y for x in ys for y in ys)
ys = [10]
print(list(g2))
```

输出什么？

## A
**输出。**

```
[1, 2, 3, 4]
[11, 12]
```

**为什么。**

- 生成器表达式在创建时就对最外层的可迭代对象求值并取迭代器，抓住的是当时那个列表对象，而不是名字 `xs`。
- 之后 `xs.append(4)` 改的是同一个对象，生成器看得到；`xs = [9]` 只是把名字指向别处，生成器不受影响。
- 其余部分（内层的 `ys`）推迟到消费时才求值，那时 `ys` 已指向 `[10]`，所以 `x` 取 1、2，`y` 取 10。

**语言为什么这样设计。**

- PEP 289 规定最外层先求值：这样 `(x for x in None)` 这类错误在创建时就暴露，而不是等到很晚才抛出；内层表达式可能依赖循环变量，只能推迟。
- Python 的惰性只在生成器和迭代器上显式出现，Haskell 则默认所有表达式惰性；这里是两种求值时机的折中。

**怎么写才对。**

```python
g = (x for x in list(xs))   # 要快照就先复制
```

**面试里一句话。**

A generator expression evaluates its outermost iterable immediately but everything else lazily, so later rebinding of an inner name changes the result.
