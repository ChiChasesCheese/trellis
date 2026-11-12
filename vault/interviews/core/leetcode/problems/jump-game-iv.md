---
slug: jump-game-iv
---
## Q
**LC 1345 跳跃游戏 IV**｜Hard

从下标 `0` 出发，每步可跳到 `i±1`，或任意值相同的其它下标。求到达最后一个下标的最少步数。

## A
**一句话。** 下标当节点做 BFS，同值下标的列表第一次展开后立刻清空，保证每条同值边只走一次。

```python
def min_jumps(arr):
    n = len(arr)
    if n == 1:
        return 0
    same = defaultdict(list)     # 值 -> 所有下标
    for i, v in enumerate(arr):
        same[v].append(i)

    seen = [False] * n
    seen[0] = True
    queue = deque([0])
    steps = 0
    while queue:
        steps += 1               # 本层再走一步
        for _ in range(len(queue)):
            i = queue.popleft()
            # pop：同值列表只展开一次
            for j in (*same.pop(arr[i], ()), i - 1, i + 1):
                if 0 <= j < n and not seen[j]:
                    if j == n - 1:
                        return steps
                    seen[j] = True
                    queue.append(j)
    return -1
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 不清空同值列表：全相等的数组每个节点扫 `n` 个下标，`O(n²)` 超时。
- 漏掉 `n == 1`：起点即终点，循环走不到，返回 `-1`，应为 `0`。
- 到终点要在入队时返回：此时步数已是 `steps`，等出队再算会多一步。

**追问。**
- 要输出最短路径？：用 `prev[j] = i` 记前驱，到终点后回溯。
- 起点是所有值为 `x` 的下标？：多源 BFS，初始队列放入全部起点。

**同模式。** LC 1654 到家的最少跳跃次数、LC 45 跳跃游戏 II、LC 127 单词接龙、LC 1306 跳跃游戏 III
