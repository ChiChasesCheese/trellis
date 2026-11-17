---
id: bank-iterators-pull-order
node: bank.structures.iterators
type: qa
step: 4
---
## Q
流式转换器 `convert_samples(samples)` 对每个采样产出若干事件，`compress_samples` 把相邻相同的采样合成一段。「当前采样的事件还没产完，就不读下一个采样」「读到第一个不同的采样，就产出上一段」这两条，为什么写成生成器就自然满足？违反它们的写法是什么？

## A
**谁拉才读，生成器的控制流自带这个顺序**

- **拉取式（pull）**：消费者每调一次 `next`，生成器才从上次 `yield` 之后继续往下跑。`for s in samples: yield ...` 里，只有当前采样的事件都被取走，外层循环才会推进到下一个采样。下面第二次 `next` 没有打印 `read`；
- **`compress` 的时机**：读到第一个不同的采样，上一段已经确定，立刻产出。不要为了「看看是不是最后一段」多读一个，对无穷流会一直卡住；
- **违反的写法**：开头 `samples = list(samples)`（惰性没了，内存随输入增长）；先把一个采样的所有事件收集成列表再返回；先读下一个、再产出当前的；
- **参数检查要放在调用时**：生成器函数被调用时不执行函数体，`convert_samples(samples, 0)` 的参数校验写在生成器里，要到第一次 `next` 才抛。做法是外层普通函数先校验，再返回内层生成器；
- **内存**：只保留当前采样和少量状态，与栈深成正比，与流长度无关。

```python
def source():
    for ts in (1, 2, 3):
        print("  read", ts); yield ts

def convert(samples):                                # 一个采样产出两个事件
    for s in samples:
        yield f"end {s}"
        yield f"start {s}"

g = convert(source())
for _ in range(3): print(next(g))                    # 第 2 次 next 不读，第 3 次才读 2
```

<details class="pt"><summary>延伸</summary>

「读到第一个不同的采样就产出」不等于不读：判断「不同」本来就要读到它，所以一段的输出要等到下一个不同的采样出现才有；这是合同允许的延迟，不是多余的预读。生成器版的转换与压缩，和手写迭代器类相比样板少得多，惰性规则靠控制流保证，不靠记性。完整合同见 [[solution-lcp-stack-trace-stream|流式调用栈处理器（Streaming Stack Trace Processor）]]。

</details>

**知识点：**迭代器设计（Iterator Design）
