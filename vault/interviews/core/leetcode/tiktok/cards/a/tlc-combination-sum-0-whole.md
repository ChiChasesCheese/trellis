---
id: tlc-combination-sum-0-whole
node: a.combination-sum
type: qa
---
## Q
**LC 39 组合总和**｜Medium · TikTok·字节 高频

给一个**无重复元素**的整数数组 `candidates` 和目标整数 `target`，找出所有和为 `target` 的不同组合，任意顺序返回。`candidates` 里的同一个数字可以被无限次重复选取；只要有一个数字的选取次数不同，就是不同的组合。保证和为 `target` 的不同组合数少于 `150` 个。`1 <= candidates.length <= 30`，`2 <= candidates[i] <= 40`，`candidates` 的所有元素互不相同，`1 <= target <= 40`。例：`[2,3,6,7], 7` → `[[2,2,3],[7]]`；`[2,3,5], 8` → `[[2,2,2,2],[2,3,3],[3,5]]`；`[2], 1` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 回溯（backtracking）：按下标顺序依次决定「选哪个数」，每次递归时只允许选**当前下标及之后**的数（避免同一组合以不同顺序重复出现），同一个数可以连续选所以递归时下标不加一；先排序，一旦当前数超过剩余目标就 `break`。

**识别。** 「找出所有组合」「可重复选取」是回溯的信号；"所有方案"决定了无法用动态规划只求数量。`target <= 40`、`candidates[i] >= 2`，最深递归层数 `target / 2 = 20`，不会爆栈。

**推导。** 暴力：每一步从所有候选里选一个，直到和不小于目标，得到的是**排列**（`[2,2,3]` 与 `[2,3,2]` 重复）。去重的洞察：约定组合内部的元素按候选数组的下标非递减顺序出现。具体做法是递归函数带一个 `start`，本层只能选 `candidates[start:]` 里的数，选了第 `i` 个之后传 `i`（允许再选它自己）。排序后，若 `candidates[i] > remain`，后面更大的数也放不下，直接 `break` 剪枝。

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates = sorted(candidates)                # 排序后，一旦某个数放不下，后面更大的都放不下
    result: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            result.append(path[:])                 # 存副本：path 之后还会被修改
            return
        for i in range(start, len(candidates)):
            x = candidates[i]
            if x > remain:
                break                              # 剪枝：后面的数只会更大
            path.append(x)
            dfs(i, remain - x)                     # 传 i 而不是 i+1：同一个数可以重复选
            path.pop()

    dfs(0, target)
    return result
```

运行：`[2,3,6,7], 7` → `[[2,2,3],[7]]`；`[2,3,5], 8` → `[[2,2,2,2],[2,3,3],[3,5]]`；`[2], 1` → `[]`；`[7,3,2], 18` 的前三个组合是 `[2,2,2,2,2,2,2,2,2]`、`[2,2,2,2,2,2,3,3]`、`[2,2,2,2,3,7]`。

**复杂度。** 时间最坏约 `O(组合数 * 长度)`，搜索树节点数由 `target / min(candidates)` 层深和分支数限制，上界指数级但被 `target <= 40` 压住；空间 `O(target / min(candidates))`（递归栈和 `path`）。

**易错点。**
- 每层都从 `0` 开始选会得到排列：`[2,3,6,7], 7` 得到 `[[2,2,3],[2,3,2],[3,2,2],[7]]`，共 4 个，正确是 2 个。
- 递归传 `i + 1` 就变成每个数只能用一次，漏掉重复使用：`[2,3,6,7], 7` 只得到 `[[7]]`。
- `result.append(path)` 没有拷贝，之后 `path` 被修改，所有结果都变成同一个（最后为空）列表。

**追问。**
- 每个数只能用一次且数组含重复（LC 40）：排序后，同一层里跳过与前一个相同的数，递归传 `i + 1`。
- 只问有多少种组合（LC 518 零钱兑换 II）：动态规划，外层遍历数、内层遍历和，`dp[t] += dp[t - x]`。
- 只问是否存在或最少个数：不用回溯，动态规划即可。

**同模式。** LC 40 组合总和 II、LC 216 组合总和 III、LC 78 子集、LC 46 全排列、LC 518 零钱兑换 II。
