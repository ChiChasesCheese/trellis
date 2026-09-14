---
id: cc-toolbox-deque-monotonic-max
node: toolbox.deque
type: qa
---
## Q
Maximum of every window of size k over 10^6 numbers. A heap is O(n log n) with stale entries. What is O(n)?

## A
**A monotonic deque holding *indices* whose values are decreasing.**

```python
for i, x in enumerate(a):
    while dq and a[dq[-1]] <= x:
        dq.pop()                       # x dominates: those can never be the max again
    dq.append(i)
    if dq[0] <= i - k:
        dq.popleft()                   # fell out of the window on the left
    if i >= k - 1:
        out.append(a[dq[0]])
```

- Each index is pushed once and popped once → O(n) total, despite the inner `while`.
- Store **indices**, not values, or the "left of the window" test is impossible.
- `<=` versus `<` on the dominance pop decides which of several equal maxima survives — irrelevant for the value, decisive if you also report the position.
- Flip the comparison for a sliding minimum; the same skeleton also gives "max of every prefix ending here under a constraint".

## Q zh
在 10^6 个数上求每个大小为 k 的窗口的最大值。堆是 O(n log n) 且带过期条目。O(n) 的做法是什么？

## A zh
**一个单调 deque，保存值递减的*下标*。**

```python
for i, x in enumerate(a):
    while dq and a[dq[-1]] <= x:
        dq.pop()                       # x 更优：那些再也不可能成为最大值
    dq.append(i)
    if dq[0] <= i - k:
        dq.popleft()                   # 从左侧掉出窗口
    if i >= k - 1:
        out.append(a[dq[0]])
```

- 每个下标入队一次、出队一次 → 总体 O(n)，尽管里面有 `while`。
- 存**下标**而不是值，否则「掉出窗口左侧」这个判断根本没法做。
- 淘汰时用 `<=` 还是 `<` 决定多个相等最大值中哪个存活 —— 对值无所谓，对同时要报告位置则是决定性的。
- 把比较符反过来就是滑动最小值；同样的骨架也能给出「在约束下以此处结尾的前缀最大值」。
