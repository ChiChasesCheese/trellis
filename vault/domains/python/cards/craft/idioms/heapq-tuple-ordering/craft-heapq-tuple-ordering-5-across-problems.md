---
id: craft-heapq-tuple-ordering-5-across-problems
node: craft.idioms.heapq-tuple-ordering
type: qa
step: 5
---
## Q
**heapq 的元组序 · 缓存、线程池、分账、额度里同一个排序键设计**｜写法

TTL 缓存的过期堆、线程池的任务队列、分账的债权人堆、额度扣费的发放堆，元素长得都不一样。它们是怎么处理「相等时怎么办」「没有大顶堆」「载荷不可比较」的？

## A
**要点。** 同一个套路：键写成元组，**主序在前、tie-break 序号在中、载荷在最后**。变的只是用哪种手段保证载荷不被比较、以及主序怎么取向。

```python
# ttl-cache：列表 [截止时刻, 序号, key]
entry = [deadline, next(self._counter), key]
heapq.heappush(self._heap, entry)

# thread-pool：dataclass(order=True)，函数和 Future 不参与比较
priority: float
sequence: int
fn: Callable[..., Any] = field(compare=False)

# splitwise：负号做大顶堆，序号做 tie-break
heapq.heappush(creditors, (-balance, next(tie), user))

# credit-token-balance：None 用布尔标记排到最后
return (g.expires_at is None, g.expires_at, g.at, g.id)
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

另外，邮箱里用 `(-严重度, 序号, 事件)`，严重度高的先出、同级先到先出；任务调度器的 `_HeapEntry` 把「到期时间 → 优先级 → 序号 → id」四栏写成数据类字段。LeetCode 上同一技巧出现在单线程 CPU（`(处理时长, 下标)`）、会议室 II、积压订单。

**见于。** ttl-cache、thread-pool、splitwise、credit-token-balance、task-scheduler、amz-emergency-pubsub。

**信号。** 用 `heapq` 且元素里有对象、函数、可能为 `None` 的值；需求里出现「同一时刻先提交的先执行」「高优先级先」「永不过期放最后」。
