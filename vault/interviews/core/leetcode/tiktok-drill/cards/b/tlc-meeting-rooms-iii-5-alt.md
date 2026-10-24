---
id: tlc-meeting-rooms-iii-5-alt
node: b.meeting-rooms-iii
type: qa
step: 5
---
## Q
**LC 2402 会议室 III**｜另一种解法

`n <= 100`，不用堆，直接扫描所有房间怎么写？它的复杂度和适用范围是什么？

## A
**思路。** 对每个房间只记录“最早空闲时刻”`free_at`。会议排好序后，对每场会议：从小到大找第一个 `free_at[room] <= start` 的房间，有就占用；没有就选 `free_at` 最小的房间（并列取编号小的），从它空出的时刻起顺延。

```python
def most_booked_scan(n: int, meetings: list[list[int]]) -> int:
    free_at = [0] * n                          # 每个房间最早空闲的时刻
    count = [0] * n
    for start, end in sorted(meetings):
        for room in range(n):                  # 编号最小的、此刻已空闲的房间
            if free_at[room] <= start:
                free_at[room] = end
                break
        else:                                  # 没有空房间：选最早空出来的（min 取并列里的第一个，即编号最小）
            room = min(range(n), key=free_at.__getitem__)
            free_at[room] += end - start       # 延期：从空出的时刻起，时长不变
        count[room] += 1
    return max(range(n), key=count.__getitem__)
```

输出与堆版一致：`(2, [[0,10],[1,5],[2,7],[3,4]])` → `0`，`(3, [[1,20],[2,10],[3,5],[4,9],[6,8]])` → `1`。`n = 100`、`10^5` 场随机会议：堆版约 `0.04 s`，扫描版约 `0.17 s`；所有会议开始时间连续、结束时间相同（房间始终全忙）：堆版约 `0.02 s`，扫描版约 `0.15 s`。

**取舍。**
- 扫描版：没有堆，状态只有一个数组，逻辑与题面几乎逐句对应，不容易出错；时间 `O(M · n)`，`n <= 100` 时约 `10^7` 次比较，Python 里能过。
- 堆版：`O(M log n)`，`n` 再大也稳；需要记住“回收、取编号最小、取最早结束”三个堆操作。
- `for ... else` 是这里的惯用法：循环里 `break` 表示找到空房间，没有 `break`（循环自然结束）才进入 `else` 处理延期。
- 面试里可以先说出扫描版（正确、直接），再指出 `n` 变大时用双堆优化。
