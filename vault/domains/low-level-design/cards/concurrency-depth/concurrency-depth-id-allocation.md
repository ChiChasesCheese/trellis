---
id: concurrency-depth-id-allocation
node: concurrency-depth.safe-structures
type: qa
step: 1
---
## Q
评论服务要发递增的评论 ID。`next(itertools.count())`、`self._next += 1`、加锁的计数器，三种取号哪些能在多线程下用？失败的请求要不要烧掉一个号？

## A
**取号要原子，而且放在最后一个可能抛错的语句之后**

- **`next(itertools.count(1))`**：8 线程各取 5000 个，重复 ID 在 3.11 和 3.14t 上都是 0/100 轮。这是 CPython 的实现行为，文档没有保证，别把正确性押在它上；
- **`v = n; n = v + 1`**：3.11 上默认和 1e-6 两种间隔都是 0/100（缺口里没有切换点，被 GIL 藏住）；3.14t 上 100/100 轮出现重复 ID；
- **加锁的计数器**：取号和自增在同一个 `with lock` 里，两个构建上都是 0/100，行为有文档可依；
- **原子不等于顺序一致**：线程 A 先取 5 号，线程 B 取 6 号并先写入，读线程会先看到 6 后看到 5。需要“已写入的 ID 一定连续”就把取号和写入放在同一个临界区；
- **失败不烧号**：校验（帖子是否存在、文本是否合法）都在取号之前做完，取号是临界区里最后一个可能失败的步骤，这样 ID 序列没有空洞。

```python
import threading

class Comments:
    def __init__(self, posts):
        self._lock, self._next = threading.Lock(), 1
        self._posts, self._rows = set(posts), {}
    def add(self, post_id, text):
        with self._lock:
            if post_id not in self._posts:      # 会抛错的检查在前
                raise KeyError(post_id)
            cid, self._next = self._next, self._next + 1   # 取号在后
            self._rows[cid] = (post_id, text)
            return cid
```

<details class="pt"><summary>延伸</summary>

多个进程或实例各自发号会撞车。ID 交给共享存储：数据库自增主键、序列，或者 UUID。

</details>

**知识点：**线程安全结构的写法（Thread-Safe Structures）
