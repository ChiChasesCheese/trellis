---
id: uth-python-exceptions-context-4-with
node: python.exceptions-context
type: qa
step: 4
---
## Q
**with 背后是什么**｜Python · CPython 3.14

`with open(path) as f:` 块里抛了异常，文件为什么也会被关掉？自己写一个能放进 `with` 的对象，要实现什么？

## A
**背景。** 清理逻辑常写成 `try/finally`，可每处都手写，既啰嗦又容易忘。想把「进门做什么、出门做什么」打包进一个能复用的对象。

**结构。** `with` 要求对象有两个方法：`__enter__`（进门，返回值绑给 `as` 后面的名字）和 `__exit__`（出门，只要 `__enter__` 成功返回就一定会调用）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<text x="52" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">进门</text>
<text x="288" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一定会调用</text>
<rect x="10" y="28" width="84" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="52" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">__enter__</text>
<rect x="128" y="28" width="84" height="34" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块内代码</text>
<rect x="246" y="28" width="84" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="288" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">__exit__</text>
<line x1="94" y1="45" x2="122.0" y2="45.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128,45 122.0,48.0 122.0,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="212" y1="45" x2="240.0" y2="45.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="246,45 240.0,48.0 240.0,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="10" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">正常离开 传 (None, None, None)</text>
<text x="10" y="114" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">抛异常离开 传 (类型, 异常, 回溯)</text>
</svg>
```

**细节。**

- `__exit__` 返回真值，异常就被吞掉，`with` 后面的代码继续执行；返回假值，异常继续往外抛。
- 两个方法是在对象的类型上查找的，临时给某个实例挂方法没用。
- `@contextlib.contextmanager` 把生成器拆成两半：`yield` 之前是进门，之后是出门；块里的异常会在 `yield` 那一行重新抛出。

**坑。** 生成器写法里 `yield` 要包进 `try/finally`，否则块内一出错，`yield` 之后的清理就被跳过：

```python
@contextmanager
def tmp():
    print("enter")
    try:
        yield
    finally:
        print("cleanup")   # 去掉 try/finally：块里出错时不会打印
```

**对应 LeetCode：** 无直接对应的题
