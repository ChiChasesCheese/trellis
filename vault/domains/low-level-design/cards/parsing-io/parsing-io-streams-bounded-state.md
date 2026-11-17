---
id: parsing-io-streams-bounded-state
node: parsing-io.streams
type: qa
step: 4
---
## Q
要对一路不会结束的采样流计算「最近 3 个值的最大值」。把所有采样先收进列表再算，错在哪？流式处理器应该保留什么状态？

## A
**只保留下一步需要的状态，其余立刻丢掉**

- **列表的问题**：流可能永远不结束；就算会结束，内存也随流的长度增长；
- **窗口状态**：`deque(maxlen=n)` 满了之后每 `append` 一个新值自动挤掉最老的一个，内存固定为 n；
- **先问「输出只依赖什么」**：窗口最大值只依赖最近 n 个；折叠相同的连续栈只依赖上一个栈和一个计数；
- **丢掉的状态不能再用**：窗口之前的值已经不在了，不要写出需要回头查的逻辑；需要回头就得保留，内存就不再有界；
- **用生成器写**：一个输入进来、零个或多个输出出去，调用方想要多少就拉多少。

```python
from collections import deque

def moving_max(stream, n: int):
    win = deque(maxlen=n)                  # 状态只有最近 n 个值
    for x in stream:
        win.append(x)
        yield max(win)

print(list(moving_max(iter([3, 1, 4, 1, 5, 9, 2, 6]), 3)))   # [3, 3, 4, 4, 5, 9, 9, 9]
```

<details class="pt"><summary>延伸</summary>

测试这类处理器时，写一个只看完整历史、直接按定义计算的朴素参照，用随机流对拍；增量实现里的状态 bug 在手写例子里很难碰到。

</details>

**知识点：**流式处理大文件（Streaming Large Files）
