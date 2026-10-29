---
id: uth-compose-ring-buffer-3-core-code
node: compose.ring-buffer
type: qa
step: 3
---
## Q
**序号版环形缓冲区的最小实现**｜Linux kfifo · v6.12（简化）

把环形缓冲区写成一个 Python 类：每个操作按什么顺序改哪些结构？

## A
**不变量。**

- `0 <= write - read <= 容量`
- `write` 只由生产者改，`read` 只由消费者改
- 生产者先写槽、再推进 `write`；消费者先取槽、再推进 `read`。推进序号就是把槽「交出去」，所以必须排在最后，内核 `kfifo` 在两步之间放一道写内存屏障 `smp_wmb()` 保证次序

**顺序。** `offer`：判满，写槽，`write += 1`。`poll`：判空，取槽，`read += 1`。

```python
class RingBuffer:
    def __init__(self, size: int) -> None:
        assert size > 0 and size & (size - 1) == 0, "容量必须是 2 的幂"
        self.buf: list[object | None] = [None] * size   # 启动时一次分配好
        self.mask = size - 1                            # size = 8 时 mask = 0b111
        self.write = 0                                  # 已写入的总个数，只增不减
        self.read = 0                                   # 已读走的总个数，只增不减

    def offer(self, x: object) -> bool:
        if self.write - self.read == len(self.buf):     # 满：写入数 - 读走数 = 容量
            return False
        self.buf[self.write & self.mask] = x            # 先写槽 ...
        self.write += 1                                 # ... 再推进序号，消费者才看得到
        return True

    def poll(self) -> object | None:
        if self.read == self.write:                     # 空：两个序号相等
            return None
        i = self.read & self.mask
        x, self.buf[i] = self.buf[i], None              # 先取走并清槽 ...
        self.read += 1                                  # ... 再推进序号，槽才还给生产者
        return x
```

**坑。** 容量不是 2 的幂时 `& mask` 会算错下标，所以构造时就要检查。这里用 `None` 表示槽里没有东西，所以不能存 `None`。

**对应 LeetCode：** 无直接对应的题
