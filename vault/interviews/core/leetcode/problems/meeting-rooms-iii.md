---
slug: meeting-rooms-iii
---
## Q
**LC 2402 会议室 III**｜Hard

`n` 个会议室，会议按开始时间依次入编号最小的空房，没有空房就延期到最早空出的房间并保持时长。返回举办次数最多的房间，并列取编号最小。

## A
**一句话。** 按开始时间排序，两个堆：空闲房间的最小堆，占用房间按 `(结束时间, 编号)` 的最小堆。

```python
def most_booked(n, meetings):
    free = list(range(n))     # 空闲房间号，升序即堆
    busy = []                 # (结束时间, 房间号)
    count = [0] * n
    for start, end in sorted(meetings):
        while busy and busy[0][0] <= start:   # 半开区间
            heappush(free, heappop(busy)[1])
        if free:
            room = heappop(free)
            finish = end
        else:
            ready, room = heappop(busy)       # 最早空出的房间
            finish = ready + (end - start)    # 延期，时长不变
        count[room] += 1
        heappush(busy, (finish, room))
    return max(range(n), key=count.__getitem__)  # 并列取第一个
```

**复杂度。** 时间 `O(M log M)`，空间 `O(n)`。

**易错点。**
- 延期会议的结束时间仍写 `end`：忘了时长不变，`n=2`、`[[0,10],[1,5],[2,7],[3,4]]` 得 `1`，应为 `0`。
- 回收条件写成 `busy[0][0] < start`：半开区间在结束时刻房间已空，要用 `<=`。

**追问。**
- 会议不按开始时间到达？：用优先队列存等待中的会议，房间空出时弹出开始最早的，复杂度同阶。

**同模式。** LC 253 会议室 II、LC 1834 单线程 CPU、LC 1882 使用服务器处理任务、LC 2406 将区间分为最少组数
