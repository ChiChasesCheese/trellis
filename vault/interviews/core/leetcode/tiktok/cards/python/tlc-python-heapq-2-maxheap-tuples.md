---
id: tlc-python-heapq-2-maxheap-tuples
node: python.heapq
type: qa
step: 2
---
## Q
**Python 工具箱｜最大堆与元组入堆**

怎样用 `heapq` 得到最大堆？往堆里放 `(优先级, 对象)` 元组时，优先级相同会出什么问题，怎样避免？

## A
**最大堆**：存 `-x`，弹出后再取负。

```python
import heapq
mh = [-x for x in [3, 1, 4, 1, 5]]
heapq.heapify(mh)
print(-heapq.heappop(mh))   # 5
```

**元组入堆**按字典序比较：先比第一项，相同再比第二项……如果比到的那一项是没有 `<` 的对象，就报错。

```python
import heapq, itertools
class N:                       # 没有定义 __lt__ 的普通对象
    def __init__(self, v: int) -> None: self.v = v
h: list = []
heapq.heappush(h, (1, N(1)))
try:
    heapq.heappush(h, (1, N(2)))   # 优先级同为 1，要比较两个 N
except TypeError as e:
    print(e)                       # '<' not supported between instances of 'N' and 'N'
cnt = itertools.count()
h = []
heapq.heappush(h, (1, next(cnt), N(1)))   # 中间插入自增序号：永远分出胜负，且先进先出
heapq.heappush(h, (1, next(cnt), N(2)))
print(heapq.heappop(h)[2].v)               # 1
```

- 合并 K 个链表（LC 23）：`ListNode` 不可比较，入堆写 `(node.val, i, node)`，`i` 是链表编号。
- 字符串做最大堆不能取负：改存 `(-ord(c), c)`，或自定义带 `__lt__` 的类；按频次的最大堆存 `(-count, ch)`，LC 1405、767 都用这个写法。
- 取负只适用于数值；要在最大堆里同时按多个字段比较，每个数值字段都取负，字符串字段无法取负。
