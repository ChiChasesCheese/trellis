---
id: craft-bisect-sorted-lists-4-check-neighbours-only
node: craft.idioms.bisect-sorted-lists
type: qa
step: 4
---
## Q
**bisect 与有序列表 · 插入新区间时为什么只需要检查左右两个邻居**｜写法

车辆的行程排程是一条按时间有序、互相自洽的链。新增一段行程时，租车排程用 `bisect` 找到插入点，只复查「前一段、这一段、后一段」。为什么这样就够了？每次整条重排再整体校验有什么代价？

## A
**要点。** 这是归纳：链在插入之前已经有序且自洽，那么新元素只可能与**紧挨着它的左右邻居**冲突，更远的元素与它之间隔着邻居，邻居之间已经自洽，不会因为新元素而改变。所以只查两个邻居，O(log n) 找插入点加 O(1) 检查。整条重排再整体校验是 O(n log n)，且每次预订都付一遍。

```python
class Calendar:
    """My Calendar I: 预订 [start, end)，与已有预订重叠就拒绝。"""
    def __init__(self) -> None:
        self._b: list[tuple[int, int]] = []     # 按 start 有序，且互不重叠

    def book(self, start: int, end: int) -> bool:
        i = bisect_left(self._b, (start, end))  # 插入点
        prev = self._b[i - 1] if i > 0 else None
        nxt = self._b[i] if i < len(self._b) else None
        # 链本来就有序且互不重叠: 新区间只可能与左右邻居冲突
        if prev and prev[1] > start:
            return False
        if nxt and nxt[0] < end:
            return False
        insort(self._b, (start, end))
        return True

c = Calendar()
print(c.book(10, 20), c.book(15, 25), c.book(20, 30), c.book(5, 10), c.book(0, 40))
```

实际输出：

```
True False True True False
```

**前提。** 这个捷径只在「已有的链本身是合法的」时成立。租车排程里，链暂时不自洽的特殊场景（强制插入）仍走整条重排的慢路径，保留了正确性。写捷径时要写清楚它依赖的前提，并留着慢路径兜底、用于测试对拍。

**信号。** LeetCode 的 My Calendar I、会议室预订、排课：一个有序的区间集合，每次判断新区间会不会和已有的重叠。
