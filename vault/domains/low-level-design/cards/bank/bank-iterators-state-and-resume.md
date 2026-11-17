---
id: bank-iterators-state-and-resume
node: bank.structures.iterators
type: qa
step: 1
---
## Q
遍历到一半要存档、换个进程接着走，为什么用生成器写不了？迭代器类该怎么写，`__iter__` 应该返回什么？

## A
**状态放进字段，才能存档和续跑**

- **迭代器协议**：`__next__` 给出下一个元素，耗尽时抛 `StopIteration`；`__iter__` 返回迭代器自己，`for` 才能直接用它。代价是只能走一遍；
- **可迭代对象不同**：容器类的 `__iter__` 每次返回一个新的迭代器，能反复遍历。把容器的 `__iter__` 写成 `return self`，第二个循环是空的，而且不报错；
- **生成器的状态在帧里**：局部变量和执行位置藏在帧对象里，`pickle`、`copy.copy`、`copy.deepcopy` 都拒绝它（`TypeError: cannot pickle 'generator' object`）。要存档，状态就不能藏在帧里；
- **显式状态**：类把「位置」放在字段里，存档就是读出这个整数，续跑就是用它重新构造。下面 `Cursor` 的全部状态是一个整数；
- **状态复杂时导出副本**：状态是上一个栈、每层的连续次数这类列表时，快照导出的是复制品，不是内部引用，恢复时也复制一份回去，两个恢复出来的迭代器才不会共享状态。

```python
class Cursor:
    def __init__(self, items, pos=0):
        self.items, self.pos = tuple(items), pos     # 全部状态：一个元组加一个整数
    def __iter__(self): return self                  # 迭代器：自己就是迭代器
    def __next__(self):
        if self.pos >= len(self.items): raise StopIteration
        self.pos += 1
        return self.items[self.pos - 1]

c = Cursor("abcde")
print(next(c), next(c))                              # a b
saved = c.pos                                        # 存档：2
print(list(Cursor("abcde", saved)))                  # ['c', 'd', 'e']：从存档续跑
print(list(c), list(c))                              # ['c', 'd', 'e'] []：只能走一遍
```

<details class="pt"><summary>延伸</summary>

「续跑的输出要和不中断逐字相同」要用随机输入、在每个位置存一次档再续跑来证明，只测几个例子不够。流式调用栈处理器的快照就是这样验证的，见 [[solution-lcp-stack-trace-stream|流式调用栈处理器（Streaming Stack Trace Processor）]]。

</details>

**知识点：**迭代器设计（Iterator Design）
