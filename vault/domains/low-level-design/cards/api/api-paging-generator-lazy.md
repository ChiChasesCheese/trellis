---
id: api-paging-generator-lazy
node: api.paging-iteration
type: qa
step: 4
---
## Q
`convert_samples(samples, confirmations)` 写成生成器函数，参数 `confirmations` 是负数。调用它时没有任何异常，等遍历到第一个元素才报错。为什么？怎样让校验在调用时就发生？

## A
**生成器函数的函数体，要等第一次 `next` 才开始执行**

- **调用只造出生成器对象**：`gen = convert(...)` 一行代码也没执行，参数检查写在生成器里，就推迟到第一次迭代；
- **推迟的后果**：错误出现在离调用很远的地方，堆栈指不到出错的参数；
- **拆成两层**：外层普通函数负责校验和取快照，再返回内层生成器；
- **同理，输入被惰性消费**：外层校验完才开始读 `samples`，调用时没有读取任何数据；
- **生成器只能遍历一次**：第二遍是空的，不报错；接口的文档要写“只能遍历一次”，要多次用就返回列表或可重新遍历的对象。

```python
def lazy(items, n):
    if n < 1: raise ValueError("bad n")                # 推迟到第一次 next
    yield from items

def eager(items, n):
    if n < 1: raise ValueError("bad n")                # 调用时就报
    return (x for x in items)

g = lazy([1], 0)                                       # 没报错
try: next(g)
except ValueError as e: print("lazy fails late:", e)
try: eager([1], 0)
except ValueError as e: print("eager fails now:", e)
```

**知识点：**大结果集接口（Pagination & Iteration）
