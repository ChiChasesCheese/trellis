---
id: craft-lazy-deletion-heap-5-scales-max-stack
node: craft.patterns.lazy-deletion-heap
type: qa
step: 5
---
## Q
**惰性删除堆 · 从 Max Stack 到延迟队列和 LSM 树**｜模式

LeetCode 的 Max Stack 要支持 `popMax`（删掉最大值，且是最近的那个）。栈和堆里各存一份元素时，删除怎么做？同样的想法在延迟队列和存储引擎里叫什么？

## A
**要点。** 两个结构各存一份，删除时只在一边真删，另一边标记墓碑，每一边在自己被访问时清理墓碑：`pop` 把 id 放进 `dead`，堆在下次取最大值时发现堆顶 id 已死就弹掉；`popMax` 反过来。

```python
def pop(self):
    self._clean_stack()                 # 栈顶若是已死元素先丢掉
    i, x = self.stack.pop()
    self.dead.add(i)                    # 堆里那一份成为墓碑
    return x

def popMax(self):
    self._clean_heap()
    negx, negi = heapq.heappop(self.heap)
    self.dead.add(-negi)                # 栈里那一份成为墓碑
    return -negx
```

压入 5、1、5，依次 `popMax`、`pop`、`peekMax`：

```
5 1 5
```

**尺度对照。** 堆里的 id 集合 → 任务调度器的取消表 → 用 Redis 有序集合等做的延迟队列里「打删除标记，消费时过滤」→ LSM 树（日志结构合并树）的墓碑，由后台压实（compaction）才真正回收空间。

**变化。** 单进程里墓碑和压实都在同一个锁下；存储引擎里墓碑要保留到所有旧版本的数据都被合并掉才能删，否则被删的数据会「复活」。

**信号。** 容器只支持追加或弹出，而业务要求取消、撤销、覆盖。
