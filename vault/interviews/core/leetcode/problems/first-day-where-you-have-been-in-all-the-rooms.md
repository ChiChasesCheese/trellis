---
slug: first-day-where-you-have-been-in-all-the-rooms
---
## Q
**LC 1997 访问完所有房间的第一天**｜Medium

访问房间 `i`：次数为奇数则次日去 `nextVisit[i]`，为偶数则次日去 `i+1`（`nextVisit[i] <= i`）。求第一次访问完所有房间的日期，对 `10^9+7` 取余。

## A
**一句话。** 线性 DP：第一次到 `i` 会被送回 `nextVisit[i]`，要把那段路再走一遍才能到 `i+1`。

```python
def first_day_been_in_all_rooms(next_visit):
    mod = 10**9 + 7
    n = len(next_visit)
    first = [0] * n               # first[i]：首次到房间 i 的日期
    for i in range(n - 1):
        # 回到 nv 再走回 i 要 first[i] - first[nv]，再 +1 +1
        nv = next_visit[i]
        first[i + 1] = (2 * first[i] - first[nv] + 2) % mod
    return first[-1]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 漏减 `first[nv]`，写成 `2 * first[i] + 2`：`[0,1,2,0]` 得 `14`，应为 `6`。
- 取模后的差为负：Python 的 `%` 安全；C++ / Java 要写 `(… + mod) % mod`。
- 答案取 `first[n]`：应为 `first[n-1]`，到最后一间那天就访问完了。

**追问。**
- 怎么验证推导？：小 `n` 直接模拟（记每间访问次数，按奇偶决定下一间），与公式比较。
- 用前缀和怎么写？：设 `step[i] = first[i+1] - first[i]`，则 `step[i] = 2 + 前缀差`，免去回查，思路等价。

**同模式。** LC 70 爬楼梯、LC 509 斐波那契数、LC 1137 第 N 个泰波那契数、LC 873 最长的斐波那契子序列的长度
