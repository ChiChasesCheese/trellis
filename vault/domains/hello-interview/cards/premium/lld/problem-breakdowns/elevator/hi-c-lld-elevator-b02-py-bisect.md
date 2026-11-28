---
id: hi-c-lld-elevator-b02-py-bisect
node: lld.problem-breakdowns.elevator.beyond
type: qa
step: 2
---
## Q
**电梯系统 · Python：用有序列表和二分找"前方的下一站"**｜拓展 · 加分

每拍都遍历全部请求判断"前方有没有请求"，请求很多时怎么优化？代价是什么？

## A
```python
import bisect


class Stops:
    def __init__(self) -> None:
        self.floors: list[int] = []         # 始终保持升序、无重复

    def add(self, f: int) -> None:
        i = bisect.bisect_left(self.floors, f)          # O(log n) 找位置
        if i == len(self.floors) or self.floors[i] != f:
            self.floors.insert(i, f)                    # 插入要移动后面的元素，O(n) 但是内存拷贝

    def next_above(self, cur: int) -> int | None:
        i = bisect.bisect_right(self.floors, cur)       # 第一个严格大于 cur 的位置
        return self.floors[i] if i < len(self.floors) else None

    def next_below(self, cur: int) -> int | None:
        i = bisect.bisect_left(self.floors, cur)        # 第一个大于等于 cur 的位置，它前一个才是严格小于
        return self.floors[i - 1] if i else None


s = Stops()
for f in (8, 3, 7, 3):
    s.add(f)
assert s.floors == [3, 7, 8]
assert s.next_above(5) == 7 and s.next_below(5) == 3
assert s.next_above(8) is None and s.next_below(3) is None   # 前方没有：该换向了
```
- **换来什么：** "前方有没有请求"和"最近的前方请求"都从 O(n) 降到 O(log n)，而且直接给出下一站。
- **代价：** 多维护一份有序结构；还要分类型（上行呼叫、下行呼叫、目的层）各一份，或在元素里带类型。
- **何时不用：** 只有 10 层，遍历十个元素比维护结构更简单也不慢；楼层很多（高层建筑群、仿真大量请求）才值得。
- **一般规律：** 先写出清晰的版本，说明何时需要优化，再给出优化方向，不要先优化。
