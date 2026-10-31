---
id: tlc-patterns-backtracking-6-variants
node: patterns.backtracking
type: qa
step: 6
---
## Q
**回溯（Backtracking）｜变形：括号生成、复原 IP、火柴拼正方形**

这三题分别用什么约束剪枝？回溯函数的参数里放什么状态？

## A
- **用计数约束让每条路径天然合法**：状态是 `(已放左括号数, 已放右括号数)`；左括号还有额度就可以放，右括号只能在**已放左括号更多**时放，不用事后检查。`n = 1..8` 的个数是卡特兰数 `1, 2, 5, 14, 42, 132, 429, 1430`（例：LC 22 括号生成）。
- **按剩余长度剪枝的分段**：分 4 段，每段 1 到 3 位，不能有前导零（单独的 `0` 除外），值 `<= 255`；剩余字符数必须在 `[剩余段数, 3 * 剩余段数]` 内，否则直接返回。`"25525511135"` → `["255.255.11.135", "255.255.111.35"]`（例：LC 93 复原 IP 地址）。
- **放进若干个桶，排序加等价状态去重**：把每根火柴放到 4 条边之一。① 总和不能被 4 整除或最长的火柴超过边长则直接 `False`；② **从大到小排序**，更早发现放不下；③ 当前边长度与前面某条边相同的，只试一次。不加剪枝，`15` 根火柴 `4^15 ≈ 10^9`，超时（例：LC 473 火柴拼正方形）。

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

**例题：** LC 473 火柴拼正方形

用数组 `matchsticks` 里的**所有**火柴拼正方形，不能折断，`1 <= matchsticks.length <= 15`，`1 <= matchsticks[i] <= 10^8`。

```python
def makesquare(matchsticks: list[int]) -> bool:
    total = sum(matchsticks)
    if total % 4:
        return False
    side = total // 4
    sticks = sorted(matchsticks, reverse=True)
    if sticks[0] > side:
        return False
    sides = [0] * 4
    def dfs(i: int) -> bool:
        if i == len(sticks):
            return True
        tried: set[int] = set()
        for j in range(4):
            if sides[j] + sticks[i] > side or sides[j] in tried:
                continue
            tried.add(sides[j])
            sides[j] += sticks[i]
            if dfs(i + 1):
                return True
            sides[j] -= sticks[i]
        return False
    return dfs(0)
```
