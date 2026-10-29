---
id: tlc-first-day-where-you-have-been-in-all-the-rooms-4-followup
node: a.first-day-where-you-have-been-in-all-the-rooms
type: qa
step: 4
---
## Q
**LC 1997 访问完所有房间的第一天**｜追问

面试官接着问：（1）你怎么确认这个递推没推错？（2）用前缀和重写，有什么好处？（3）如果不取模，`n = 10^5` 时答案有多大，Python 能直接算吗？

## A
1. **验证递推**：对小的 `n` 写一个逐天模拟的版本（记每个房间的访问次数，按奇偶决定下一个房间，直到所有房间都访问过），和公式在 `[0,0]`、`[0,0,2]`、`[0,1,2,0]` 等输入上对比，结果分别是 `2`、`6`、`6`。

```python
def simulate(next_visit: list[int]) -> int:
    n = len(next_visit)
    count = [0] * n
    seen = {0}
    day = room = 0
    while len(seen) < n:
        count[room] += 1
        room = next_visit[room] if count[room] % 2 else (room + 1) % n
        day += 1
        seen.add(room)
    return day
```

模拟的天数随 `n` 指数增长，只适合 `n` 在十几以内的小输入。
2. **前缀和写法**：令 `gap[i] = first[i+1] - first[i]`，则 `gap[i] = 2 + (first[i] - first[nv[i]])`，等于 `2` 加上 `gap[nv[i]]` 到 `gap[i-1]` 的和。把 `gap` 的前缀和存起来，递推就变成对前缀和数组的区间查询，思路等价，好处是更容易发现"为什么答案是线性递推"。
3. **不取模的大小**：`next_visit[i] = 0` 对所有 `i` 时，`first[i+1] = 2 * first[i] + 2`，`first[n-1] = 2^(n-1) * 2 - 2`，大约 `2^n`。`n = 10^5` 时有三万多位十进制数字。Python 的整数是任意精度，能算但每步要做大整数加法，整体变成平方级；所以取模要放在循环里，而不是最后一次性取。

**Python 提醒**：`(a - b) % m` 在 Python 里对正的 `m` 永远非负，但把这段逻辑翻译成 C++ / Java 时，`%` 可能得到负数，需要 `((a - b) % m + m) % m`。
