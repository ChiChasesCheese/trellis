---
id: pl-functional-generators-foundation-python-yield
node: functional.generators
type: qa
step: 2
---
## Q
Python 的 `yield`、`send` 和 `close` 是什么？生成器函数被调用时，到底执行了什么？

## A
函数体里只要出现 `yield`，它就是**生成器函数**。调用它**不会执行函数体**，只返回一个生成器对象，里面保存着函数的帧（局部变量和执行到哪一行）。每次 `next(g)`，帧从上次暂停处继续运行，直到下一个 `yield`，把值交出去再暂停。

```python
def lazy():
    print("started")
    yield 1
l = lazy()
print("created")       # 只输出 created；"started" 还没出现
```

生成器还是**双向**的：`yield` 是个表达式，`g.send(v)` 把 `v` 作为 `yield` 的结果送进去：

```python
def acc():
    total = 0
    try:
        while True:
            x = yield total
            total += x
    finally:
        print("cleanup")
g = acc(); next(g)               # 先推进到第一个 yield
g.send(5), g.send(10)            # (5, 15)
g.close()                        # 在暂停处抛 GeneratorExit，finally 执行，输出 cleanup
```

这使得生成器不仅能产出序列，还能写成**消费者**或**状态机**。后来 `async`/`await` 就是在生成器基础上长出来的：`await` 的本质是「暂停，等别人叫我继续」。

内存上，一个暂停的生成器对象很小（实测不到 300 字节，加上它引用的局部变量），而同样 10 万个整数的列表约 800 KB，这就是用生成器处理大数据的原因。
