---
slug: jump-game
---
## Q
**LC 55 跳跃游戏**｜Medium

`nums[i]` 是在下标 `i` 处最多能向前跳的步数，判断能否从第一个下标到达最后一个。

## A
**一句话。** 贪心：扫描时维护能到达的最远下标 `reach`，当前下标超过它就被卡住。

```python
def can_jump(nums):
    reach = 0                    # 目前能到的最远下标
    for i, step in enumerate(nums):
        if i > reach:
            return False         # 连 i 都够不着
        reach = max(reach, i + step)
    return True
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 漏掉 `i > reach` 检查，只在最后比较 `reach`：`[3,2,1,0,4]` 被 `0` 卡住后，`4` 仍累计进 `reach`，得 `True`，应为 `False`。
- 把 `nums[i]` 当成「必须跳这么多」：它是最多，覆盖整段区间。

**追问。**
- 可以向后跳（LC 1306）？：变成图搜索，用 BFS 或 DFS。
- 要输出一条具体路线？：更新 `reach` 时记下出发下标，再回溯。

**同模式。** LC 45 跳跃游戏 II、LC 1306 跳跃游戏 III、LC 134 加油站、LC 763 划分字母区间
