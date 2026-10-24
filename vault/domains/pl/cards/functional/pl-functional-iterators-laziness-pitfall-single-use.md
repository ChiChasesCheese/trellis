---
id: pl-functional-iterators-laziness-pitfall-single-use
node: functional.iterators-laziness
type: qa
step: 10
---
## Q
迭代器的一次性与惰性，在生产里最常见的两个事故是什么？

## A
**事故一：迭代器被消耗后再用，得到空结果，没有任何错误。**

```python
g = (x * x for x in range(4))
total = sum(g)        # 14
count = sum(1 for _ in g)   # 0：g 已经被耗尽
```

典型场景：把生成器传给函数 A 做校验（遍历了一遍），再传给函数 B 处理，B 看到的是空序列，于是什么都不做，且不报错。排查极难，因为没有异常。`map`/`filter`/`zip` 的结果同理。Java 的 Stream 在这里反而更友好——第二次用会抛 `IllegalStateException`，错误响亮；Python 的静默才危险。

**事故二：惰性把错误和副作用推迟到别处。**

```python
def read_rows(path):
    return (parse(line) for line in open(path))   # 此时文件已经打开，但还没读任何行
rows = read_rows("data.csv")
# ...很久之后：for r in rows: ...  这时解析错误才爆发，而且文件句柄一直开着
```

异常抛在使用处而不是创建处，堆栈里看不到创建者；文件句柄、数据库游标、锁被一个"还没被消费"的生成器占着。Java 的 Stream 如果没有终端操作，管道里的代码从未执行，而人们以为已经执行（比如只写了 `list.stream().map(this::save)` 忘了终端操作，数据根本没保存）。Rust 用 `#[must_use]` 把这类错误挡在编译期。

防御：
- 需要多次遍历的数据，显式 `list(...)` 或 `tuple(...)` 物化，并在函数文档里说明参数是否会被消耗；
- 资源敏感的迭代，用 `with` / try-with-resources 包住，保证消费完毕就关闭；
- Java 在代码审查里查「没有终端操作的 Stream」，Python 用类型 `Iterator` 与 `Iterable` 区分一次性与可重复。
