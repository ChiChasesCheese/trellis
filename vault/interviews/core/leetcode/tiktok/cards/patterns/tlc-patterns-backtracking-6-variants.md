---
id: tlc-patterns-backtracking-6-variants
node: patterns.backtracking
type: qa
step: 6
---
## Q
**回溯（Backtracking）｜变形：括号生成、复原 IP、组合总和 II**

这三题分别用什么约束剪枝？回溯函数的参数里放什么状态？

## A
- **用计数约束让每条路径天然合法**：状态是 `(已放左括号数, 已放右括号数)`；左括号还有额度就可以放，右括号只能在**已放左括号更多**时放，不用事后检查。`n = 1..8` 的个数是卡特兰数 `1, 2, 5, 14, 42, 132, 429, 1430`（例：LC 22 括号生成）。
- **按剩余长度剪枝的分段**：分 4 段，每段 1 到 3 位，不能有前导零（单独的 `0` 除外），值 `<= 255`；剩余字符数必须在 `[剩余段数, 3 * 剩余段数]` 内，否则直接返回。`"25525511135"` → `["255.255.11.135", "255.255.111.35"]`（例：LC 93 复原 IP 地址）。
- **排序后在同一层跳过相同的数**：先排序让相同的数相邻；每个数只能用一次，所以下一层从 `i + 1` 开始；同一层里 `i > start and nums[i] == nums[i-1]` 就跳过，因为在同一个位置上选两个值相同的数只会得到同一批组合；再加一条 `nums[i] > remain` 就 `break` 的剪枝。`[10,1,2,7,6,1,5]`，目标 `8` → `[[1,1,6],[1,2,5],[1,7],[2,6]]`（例：LC 40 组合总和 II）。

**例题：** LC 22 括号生成

给定 `n` 对括号，生成所有有效的括号组合，`1 <= n <= 8`。

```python
def generate_parenthesis(n: int) -> list[str]:
    res: list[str] = []
    path: list[str] = []
    def dfs(opened: int, closed: int) -> None:
        if len(path) == 2 * n:
            res.append("".join(path))
            return
        if opened < n:
            path.append("(")
            dfs(opened + 1, closed)
            path.pop()
        if closed < opened:
            path.append(")")
            dfs(opened, closed + 1)
            path.pop()
    dfs(0, 0)
    return res
```

**例题：** LC 93 复原 IP 地址

给只含数字的字符串 `s`（`1 <= s.length <= 20`），插入 `.` 返回所有有效 IP 地址，每段 `0..255` 且不能有前导 0。

```python
def restore_ip_addresses(s: str) -> list[str]:
    n = len(s)
    res: list[str] = []
    parts: list[str] = []
    def dfs(start: int) -> None:
        left = 4 - len(parts)
        if left == 0:
            if start == n:
                res.append(".".join(parts))
            return
        if not left <= n - start <= 3 * left:
            return
        for end in range(start + 1, min(start + 3, n) + 1):
            seg = s[start:end]
            if len(seg) > 1 and seg[0] == "0":
                break
            if int(seg) > 255:
                break
            parts.append(seg)
            dfs(end)
            parts.pop()
    dfs(0)
    return res
```

**例题：** LC 40 组合总和 II

数组 `candidates`（元素可能重复）和目标数 `target`，找出所有和为 `target` 的组合，每个元素在一个组合里最多用一次，结果里不能有重复的组合；`1 <= candidates.length <= 100`，`1 <= candidates[i] <= 50`，`1 <= target <= 30`。

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    nums = sorted(candidates)
    result: list[list[int]] = []
    path: list[int] = []
    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            result.append(path[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remain:
                break
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            dfs(i + 1, remain - nums[i])
            path.pop()
    dfs(0, target)
    return result
```
