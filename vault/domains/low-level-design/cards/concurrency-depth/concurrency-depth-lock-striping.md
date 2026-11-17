---
id: concurrency-depth-lock-striping
node: concurrency-depth.safe-structures
type: qa
step: 6
---
## Q
评论服务想让不同帖子互不阻塞，每个帖子配一把锁。`if post not in locks: locks[post] = Lock()` 这样建锁有什么问题？除了“每个 key 一把锁”，还有什么办法？

## A
**要么保证建锁本身原子，要么用固定数量的分片锁**

- **建锁本身是先检查后执行**：两个线程各建一把，各拿各的锁，同一个帖子的临界区重叠。实测（3.11，4 线程抢 200 个 key，临界区里带一次调用，100 轮）：默认间隔 0/100，1e-6 下 3/100 轮出现同一个 key 两个线程同时在临界区；3.14t 默认间隔 4/100。概率低，复现难，上线后才出现最麻烦；
- **每个 key 一把锁的代价**：锁表只增不减，帖子越多内存越大；回收锁又要先保证没人正在用它；
- **分片锁（lock striping）**：开机建好 N 把锁，`locks[hash(key) % N]` 取用，不动态建、不回收；不同 key 偶尔共用一把，代价是偶尔多等一会；
- **用固定把数换来简单**：N 取 16 或 64 够用；同一个 key 永远落在同一把锁上，所以互斥是对的；
- **一次操作碰两个 key（转账）**：示例只给单个 key；要同时拿两把锁，按分片编号排序后依次拿，两个 key 落在同一片就只拿一次，避免死锁。

```python
import threading

class StripedLocks:
    def __init__(self, n=16):
        self._locks = [threading.Lock() for _ in range(n)]
    def of(self, key):
        return self._locks[hash(key) % len(self._locks)]

stripes = StripedLocks()
with stripes.of("post-42"):
    pass                                   # 只锁这个帖子所在的分片
print(stripes.of("post-42") is stripes.of("post-42"))   # True
```

<details class="pt"><summary>延伸</summary>

`hash(str)` 每个进程随机化，同一个进程内一致就够用；若分片要跨进程对应同一把锁，用稳定的哈希（比如 `zlib.crc32`）。

</details>

**知识点：**线程安全结构的写法（Thread-Safe Structures）
