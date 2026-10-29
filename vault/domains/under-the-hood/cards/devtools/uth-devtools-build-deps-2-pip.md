---
id: uth-devtools-build-deps-2-pip
node: devtools.build-deps
type: qa
step: 2
---
## Q
**pip 的版本解析为什么要回溯**｜pip · resolvelib

两个包对同一个依赖要求不同的版本范围，pip 怎么找到一组都满足的版本？

## A
**背景。** 装包时每个包都声明自己依赖的版本范围。例：A 需要 `c >= 2`，B 需要 `c < 2`，要找出一组所有人都满意的版本。没有公式可算，只能试：先选一个版本（通常是最新的），往下走；发现冲突，就退回上一步换一个版本。这叫回溯（backtracking）。

**结构。** 本质是约束满足问题（和 SAT 同类，NP 完全）：为每个包选一个版本。pip 的求解器来自 resolvelib 库，是通用的回溯算法；pip 只负责提供候选版本和它们的依赖。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<rect x="65" y="50" width="50" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a 2</text>
<rect x="225" y="50" width="50" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a 1</text>
<path d="M104,48 Q170,24 231.3,46.3" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M236.0,48.0 L228.5,48.8 L230.8,42.6 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">全部走不通 退回换一个</text>
<rect x="25" y="108" width="50" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b 2</text>
<rect x="105" y="108" width="50" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b 1</text>
<rect x="225" y="108" width="50" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b 2</text>
<line x1="80" y1="74" x2="56" y2="108" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="100" y1="74" x2="124" y2="108" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="250" y1="74" x2="250" y2="108" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">冲突</text>
<text x="130" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">冲突</text>
<text x="250" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">成功</text>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">每层选一个版本 冲突就回退一步</text>
</svg>
```

**细节。**

- 依赖要下载 wheel（预编译包）或构建源码包才知道，不可能先拿到完整依赖树
- 所以只能边选边查：对每个候选“按需”取依赖，冲突了再回退

**为什么。** 元数据昂贵，先建全图再求解不现实；回溯式求解只付出实际走到的候选的代价。

**例题：** LC 46 全排列（同类：LC 39 组合总和）

给一个不含重复数字的数组 `nums`，返回它所有可能的全排列，顺序任意。`1 <= nums.length <= 6`。例：`[1,2,3]` → `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`。

```python
def permute(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    res: list[list[int]] = []
    path: list[int] = []                # 当前已选出的前缀
    used = [False] * n                  # used[i]：nums[i] 是否已在 path 里

    def dfs() -> None:
        if len(path) == n:
            res.append(path[:])         # 必须拷贝，path 之后还会被改
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            dfs()
            path.pop()                  # 撤销选择，回到上一层的状态
            used[i] = False

    dfs()
    return res
```
