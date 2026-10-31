---
id: tlc-jump-game-4-followup
node: p2.jump-game
type: qa
step: 4
---
## Q
**LC 55 跳跃游戏**｜追问

面试官接着问：（1）最少需要跳几次（LC 45）？（2）如果可以向前也可以向后跳（LC 1306）？（3）要输出一条具体的跳跃路线？

## A
1. **最少跳数。** 按“一跳的覆盖范围”分层贪心：`end` 是当前这一跳能到的最远边界，`far` 是下一跳能到的最远下标；扫到 `end` 时必须再跳一次，跳数加一，`end` 更新为 `far`：
```python
def jump(nums: list[int]) -> int:
    steps = end = far = 0
    for i, x in enumerate(nums[:-1]):       # 最后一个下标不需要再起跳
        far = max(far, i + x)
        if i == end:                        # 走到当前这一跳的边界：必须再跳一次
            steps += 1
            end = far
    return steps
```
`[2,3,1,1,4]` → `2`，`[2,3,0,1,4]` → `2`，`[0]` → `0`。假设题目保证一定能到达。
2. **可向后跳。** 位置之间是双向边，可达集合不再是前缀，贪心失效。把每个下标当图的节点，从起点做 BFS / DFS，访问过的位置打标记，`O(n)`。
3. **输出路线。** 更新 `reach` 时记下“是哪个下标让 `reach` 变大”，用数组 `parent` 保存；到达终点后从终点沿 `parent` 回溯到起点。

**Python 提醒**：`nums[:-1]` 切片会复制一份列表；对很长的数组可以用 `range(len(nums) - 1)` 配合下标，或 `itertools.islice(enumerate(nums), len(nums) - 1)` 避免复制。
