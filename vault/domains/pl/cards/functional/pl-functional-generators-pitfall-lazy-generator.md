---
id: pl-functional-generators-pitfall-lazy-generator
node: functional.generators
type: qa
step: 10
---
## Q
生成器的延迟执行会在生产里造成什么问题？为什么异常和清理逻辑最容易出错？

## A
生成器函数调用时不执行函数体，**所有逻辑（包括参数校验和异常）都推迟到第一次 `next`**，而且分散在每次恢复时：

```python
def gen_exc():
    yield 1
    raise ValueError("late")
g2 = gen_exc(); next(g2)       # 此时一切正常
next(g2)                       # ValueError: late 到这里才抛
```

后果：

- **错误位置错位**：在创建生成器处能想到的校验（路径是否存在、参数是否合法）要到消费时才失败，堆栈指向消费者，而不是出错的创建者。
- **清理逻辑可能不执行**：生成器里 `try/finally` 或 `with` 的清理，只有在生成器**跑完或被 `close()`** 时才执行。如果消费者中途 `break` 了然后放手，CPython 靠引用计数立刻回收会触发 `close()`，但其他实现（PyPy）或循环引用时，清理的时间不确定，文件句柄可能一直开着。
- **Go 的 `iter.Pull`**：忘记 `stop()` 就没有清理。

修法：把校验放在一个普通函数里，立刻检查，然后返回内部的生成器；

```python
def read_rows(path):
    f = open(path)                 # 立刻出错，而不是等到消费时
    def rows():
        with f:
            for line in f: yield parse(line)
    return rows()
```

资源敏感的消费用 `contextlib.closing(gen)` 包住，保证 `close()` 被调用；Go 里 `defer stop()`；Java 的 Stream 用 try-with-resources。核心规则：**凡是生成器持有外部资源，就要有显式的终结点**，不要依赖垃圾回收。
