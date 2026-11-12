---
slug: find-the-winner-of-the-circular-game
---
## Q
**LC 1823 找出游戏的获胜者**｜Medium

`n` 人围圈编号 `1..n`，从 1 号起数 `k` 个，数到的人出局，下一轮从其下一位继续，求最后留下的编号。

## A
**一句话。** 约瑟夫环的模拟：列表存人，淘汰下标是 `(idx + k - 1) % 当前人数`，弹出后同一下标就是下一轮起点。

```python
def find_the_winner(n, k):
    people = list(range(1, n + 1))
    idx = 0
    while len(people) > 1:
        idx = (idx + k - 1) % len(people)   # 环形取模
        people.pop(idx)                     # 后一人滑到 idx
    return people[0]
```

**复杂度。** 时间 `O(n²)`，空间 `O(n)`。

**易错点。**
- 下标写成 `(idx + k) % len(people)`：少减 `1`，`(5,2)` 得 `4`，应为 `3`。
- 弹出后又给 `idx` 加 `1`：会跳过下一轮的起点。

**追问。**
- 能 `O(n)` 时间、`O(1)` 空间吗？：递推 `f(1)=0`，`f(i)=(f(i-1)+k) % i`，最后加 `1`。
- 为什么递推成立？：少一个人后编号整体平移 `k`，在 `i` 人环里取模还原。

**同模式。** 剑指 Offer 62 圆圈中最后剩下的数字、LC 390 消除游戏、LC 292 Nim 游戏
