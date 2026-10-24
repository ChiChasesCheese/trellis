---
id: tlc-first-day-where-you-have-been-in-all-the-rooms-2-code
node: a.first-day-where-you-have-been-in-all-the-rooms
type: qa
step: 2
---
## Q
**LC 1997 访问完所有房间的第一天**｜写出 Python 实现

`nextVisit` 长度为 `n`（`2 <= n <= 10^5`），`0 <= nextVisit[i] <= i`。每天访问一个房间：今天访问 `i` 的累计次数为奇数，第二天去 `nextVisit[i]`；为偶数，第二天去 `(i + 1) mod n`；第 `0` 天在房间 `0`。返回第一次访问完所有房间的日期，对 `10^9 + 7` 取余。

## A
**思路。** `first[i]` 表示第一次到达房间 `i` 的日期，`first[0] = 0`。到达 `i` 后被送回 `nextVisit[i]`，重走到 `i` 的路程是 `first[i] - first[nextVisit[i]]`，再加两天（回跳一天、前进一天），得到 `first[i+1]`。

```python
def first_day_been_in_all_rooms(next_visit: list[int]) -> int:
    mod = 10**9 + 7
    n = len(next_visit)
    first = [0] * n                                # first[i] = 第一次到达房间 i 的日期
    for i in range(n - 1):
        # 第一次到 i（奇数次）-> 回到 nv = next_visit[i]，再走回 i 的时间是 first[i] - first[nv]
        # 第二次到 i（偶数次）-> 第二天去 i+1
        first[i + 1] = (2 * first[i] - first[next_visit[i]] + 2) % mod
    return first[-1]
```

运行：`[0,0]` → `2`，`[0,0,2]` → `6`，`[0,1,2,0]` → `6`；`n = 10^5`，`next_visit[i] = i` → `199998`；`n = 10^5`，全 `0` → `607723518`。

**复杂度。** 时间 `O(n)`，一次循环；空间 `O(n)`，需要按下标回查 `first`。

**写法要点。** `mod = 10**9 + 7` 写成常量避免魔法数；`first[-1]` 取最后一个房间；Python 的 `%` 对正模数返回非负值，所以中间出现 `2 * first[i] - first[nv]` 为负时也不用额外加 `mod`（在 C++ / Java 里要补）；取模放在每步里，保证数字不会增长成大整数，保持常数时间。
