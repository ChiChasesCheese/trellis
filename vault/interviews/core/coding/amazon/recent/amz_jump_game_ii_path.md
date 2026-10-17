# 跳跃游戏 II，返回路径（Jump Game II, return the jumps）

数组 `nums` 的第 i 个数表示：站在下标 i，最多可以向前跳 `nums[i]` 步。从下标 0 出发，要到达最后一个下标，求最少需要跳几次（LeetCode 45）。这一讲还要多做一步：不只返回次数，还要返回具体怎么跳的，也就是经过的下标序列。难点是把 O(n²) 的动态规划压成一次扫描，同时还能还原路径。

## 题面与约束
`nums[i]` 是从下标 i 最多向前跳的步数。从下标 0 出发，求到达最后一个下标的最少跳数。
约束：`1 <= nums.length <= 10^4`，`0 <= nums[i] <= 1000`，保证可以到达最后一个下标。

## 开场先问的澄清问题
1. 「返回路径」是返回经过的下标，还是每一步的跳跃长度？（下面返回下标序列，改成步长只需相邻两项相减。）
2. 最短路径有多条时，返回任意一条还是有规则？
3. 跳跃长度是「最多 nums[i]」还是「恰好」？（最多。）

## 最笨解
动态规划：`dp[j] = min(dp[i] + 1)`，对每个 i 更新所有它能到达的 j。时间 O(n·max(nums)) 到 O(n²)，n = 1e4 时约 1e8，勉强但慢（见代码 `_dp`，用来核对贪心的结果）。

## 逐步改进
1. **问题**：DP 对每个 i 都更新一遍所有可达点，大量重复。
2. **想法（贪心 = 隐式 BFS）**：把「跳 k 次能到的下标」看作第 k 层。第 k 层覆盖一个**连续区间**（因为从某点能到的所有点连续）。扫描这一层所有点，算出下一层的右边界 `far`。
3. **为什么有效**：扫完当前层（`i == end`）时必须再跳一次，下一层的右边界就是 `far`；跳数 +1。每个下标只访问一次，O(n)。
4. **返回路径**：每层记录「让 `far` 最大的下标」`best`，它就是这一层应当停留的下标。路径 = 起点 0，每层的 `best`，最后一个下标。
5. **为什么这样得到的路径合法且最短**：下一层的右边界由 `best` 一跳可达，所以 `best` 之后的下标能直接跳到；层数与最少跳数相等。

```python
def jump(nums):
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])                       # farthest index reachable with jumps + 1
        if i == end:                                      # left the current level: must take one more jump
            jumps += 1
            end = far
    return jumps

def jump_path(nums):
    n = len(nums)
    path, end, far, best = [], 0, 0, 0                    # best = index that attains `far`
    for i in range(n - 1):
        if i + nums[i] > far:
            far, best = i + nums[i], i
        if i == end:
            path.append(best)                             # the landing of this level = index reaching farthest
            end = far
    return path + [n - 1] if n > 1 else [0]
```

示例：`[2,3,1,1,4]`：最少 2 跳，路径 `[0,1,4]`（0 → 1 → 4）；改成「步长」就是 `[1,3]`。`[2,3,0,1,4]` 也是 2 跳。`[0]` 长度 1，0 跳，路径 `[0]`。

## 复杂度
时间 O(n)，空间 O(跳数) 用于路径（不返回路径时 O(1)）。

## senior 追问
1. **不保证可达**：循环中若 `far <= i` 且 `i == end`，则无法前进，返回 -1。
2. **要返回所有最短路径**：计数用 DP，枚举要回溯，可能指数级，需要问清是否要全部。
3. **字典序最小或最少「落脚点」的路径**：把「选最远」换成「选满足约束的最小下标」，仍在层内贪心。
4. **每个位置有代价（点权）**：贪心不再成立，改用 DP 或 Dijkstra：`dp[j] = min(dp[i] + cost[j])`，可用单调队列或线段树优化。
5. **能向前向后跳**：变成一般图的 BFS，O(n·k)；每个下标只访问一次的剪枝依然成立（visited）。
6. **数组超大且流式输入**：贪心只需 `end/far/best`，可以在线处理；路径需存 O(跳数)。

## 自测题
1. 为什么循环只到 `len(nums) - 1`？
<details><summary>答案</summary>最后一个下标已经是终点，不需要从它再跳；如果包含它，可能多算一次跳数。</details>
2. `best` 为什么记录「让 far 最大的下标」而不是「当前层最后一个下标」？
<details><summary>答案</summary>落脚点要使下一层覆盖范围最大；当前层最后一个下标不一定能跳得最远。</details>
3. 路径里相邻两项 a、b 一定满足什么？
<details><summary>答案</summary>`0 < b - a <= nums[a]`，代码测试里逐段断言了这一点。</details>
