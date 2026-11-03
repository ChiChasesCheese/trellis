---
id: craft-generators-lazy-traversal-3-single-use
node: craft.idioms.generators-lazy-traversal
type: qa
step: 3
---
## Q
**生成器与惰性遍历 · 生成器只能消费一次，API 该返回迭代器还是列表**｜写法

搜索函数 `find()` 返回迭代器，另一个函数 `paths()` 却在外面包了一层 `list(...)`。两个调用方先后遍历同一个生成器会发生什么？什么样的 API 该返回迭代器，什么样的该返回列表？

## A
**要点。** 生成器是**迭代器**（iterator）：`iter(g) is g`，遍历一次就耗尽，再遍历得到空，**不报错**。这是它最隐蔽的坑：第二个调用方静默拿到空结果。判据：结果是**流**（可能很大、调用方可能提前停、只会遍历一次）返回迭代器；结果是**值**（调用方要计数、取长度、多次遍历、排序、当快照保存）返回 `list` 或 `tuple`。

```python
def squares(n):
    for i in range(n):
        yield i * i

g = squares(3)
print("第一次遍历:", list(g))
print("第二次遍历:", list(g), "<- 已耗尽，不报错，只是空")
print("是迭代器吗: iter(g) is g ->", iter(g) is g)

# 需要多次遍历的 API: 返回 list（或 tuple），每次调用都是新的快照
def paths_iter(n): return squares(n)
def paths(n): return list(squares(n))

p = paths_iter(3)
print("返回生成器, 两个调用方共用一个:", sum(p), sum(p))
q = paths(3)
print("返回 list, 各取各的:", sum(q), sum(q))

# 生成器里的异常和副作用在「被消费时」才发生, 不是在创建时
def boom():
    print("  (函数体开始运行)")
    yield 1
    raise RuntimeError("第二次取值才出错")
b = boom()
print("创建生成器: 没有任何输出")
print(next(b))
```

实际输出：

```
第一次遍历: [0, 1, 4]
第二次遍历: [] <- 已耗尽，不报错，只是空
是迭代器吗: iter(g) is g -> True
返回生成器, 两个调用方共用一个: 5 0
返回 list, 各取各的: 5 5
创建生成器: 没有任何输出
  (函数体开始运行)
1
```

**为什么 `paths()` 包 `list`。** 它的调用方通常想要「全部路径」，要多次使用，所以在边界处物化一次。`find()` 是底层的流，由调用方决定是否物化。惰性的东西放里面，值放外面。

**易错。** 生成器函数在被迭代之前不执行函数体，所以参数校验放在生成器里，要到第一次取值才抛出，而不是调用时。需要「调用时立刻校验」，就把函数拆成两段：外层普通函数校验并返回内层生成器。
