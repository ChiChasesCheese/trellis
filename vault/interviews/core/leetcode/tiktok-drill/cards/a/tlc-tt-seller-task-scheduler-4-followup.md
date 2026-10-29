---
id: tlc-tt-seller-task-scheduler-4-followup
node: a.tt-seller-task-scheduler
type: qa
step: 4
---
## Q
**卖家任务调度器（轮转 + VIP + 优先级）**｜追问

面试官接着问：（1）VIP 的配额不是固定的 `2`，而是每个卖家有自己的权重；（2）卖家内部的高优先级任务不断到来，低优先级任务会不会饿死；（3）要支持取消某个任务，怎么改；（4）多线程同时调用怎么办？

## A
1. **加权轮转**：构造时传入 `weights: dict[str, int]`，把配额判断 `2 if seller in vip else 1` 换成 `weights.get(seller, 1)`，其余结构不变。
2. **饥饿**：会。同一个卖家内部，只要高优先级的任务持续到来，堆顶永远是它们。常见做法是老化（aging）：有效优先级随等待时间变好，例如排序键用 `priority - (now - timestamp) / T`；键随时间变化时堆不再有效，改成周期性重建，或把任务按优先级分桶、桶之间按等待时间做保底配额。
3. **取消任务**：懒删除。维护 `cancelled: set[str]`，`cancel(task_id)` 只往集合里加；堆顶弹出时若在集合里就丢弃并继续弹。若卖家因此变空，同样要退出轮转，并清零 `_served`。

```python
import heapq


def pop_valid(heap: list[tuple[int, int, int, str]], cancelled: set[str]) -> str | None:
    while heap:
        task_id = heapq.heappop(heap)[-1]
        if task_id not in cancelled:        # 没被取消才算数
            return task_id
        cancelled.discard(task_id)          # 已取消的丢掉，顺手清理集合
    return None
```

4. **并发**：所有读写同一份状态，最简单的做法是给整个对象加一把 `threading.Lock`，`receive_task` 和 `process_next_task` 各自在锁内完成；吞吐不够再按卖家分片，每片一把锁，轮转队列单独由一个线程维护。

**Python 提醒**：`heapq` 只提供最小堆，且比较的是整个元组；元组里放自增序号能避免在前面的字段都相同的时候去比较 `task_id`，既保证先到先出，也避免 `task_id` 类型不可比较时抛 `TypeError`。
