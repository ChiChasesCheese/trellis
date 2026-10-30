---
id: uth-python-mutability-args-4-backtrack-copy
node: python.mutability-args
type: qa
step: 4
---
## Q
**回溯里为什么要 res.append(path[:])**｜Python · CPython 3.14

回溯求全排列时，写 `res.append(path)`，最后得到的是一堆空列表；写成 `path[:]` 才对。为什么？

## A
**背景。** 回溯全程只用一个 `path` 列表：选一个就 `append`，退一步就 `pop`，不用每步新建列表。

**结构。** `res.append(path)` 放进去的是这个列表的指针，不是当前内容，`res` 里每个格子指着同一个对象。`path[:]` 新建一个列表，装着此刻各元素的指针（浅拷贝），之后 `path` 怎么变，这份快照都不受影响。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">res.append(path)</text>
<rect x="10" y="26" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="27" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<line x1="44" y1="38" x2="208" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,62.0 201.6,64.1 202.5,58.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="54" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="27" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<line x1="44" y1="66" x2="208" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,62.0 202.1,65.1 201.9,59.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="82" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="27" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<line x1="44" y1="94" x2="208" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,62.0 202.7,66.1 201.5,60.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="210" y="46" width="100" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">path = [ ]</text>
<text x="260" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">三个格子 同一个列表</text>
<line x1="10" y1="118" x2="330" y2="118" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="138" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">res.append(path[:])</text>
<rect x="10" y="148" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="27" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<line x1="44" y1="160" x2="208" y2="160" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,160.0 202.0,163.0 202.0,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="210" y="146" width="100" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260" y="163" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[1, 2, 3]</text>
<rect x="10" y="178" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="27" y="194" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<line x1="44" y1="190" x2="208" y2="190" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,190.0 202.0,193.0 202.0,187.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="210" y="176" width="100" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260" y="193" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[1, 3, 2]</text>
<rect x="10" y="208" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="27" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<line x1="44" y1="220" x2="208" y2="220" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,220.0 202.0,223.0 202.0,217.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="210" y="206" width="100" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260" y="223" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[2, 1, 3]</text>
<text x="170" y="244" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次拍一张快照</text>
</svg>
```

**细节。**

- 回溯跑完时 `path` 已被 `pop` 成空，`[1, 2, 3]` 的全排列写成 `res.append(path)` 就得到 6 个 `[]`。
- `path[:]`、`path.copy()`、`list(path)` 效果一样，每次花 O(len) 的时间。
- 快照不增加复杂度：结果本来就要存下这么多元素。

**坑。** 元素本身若还是可变对象（比如子列表），浅拷贝里它们仍然共享。

**例题：** LC 78 子集

给元素互不相同的整数数组 `nums`，返回它所有可能的子集（幂集），不能有重复子集。`1 <= nums.length <= 10`。例：`[1,2,3]` 得 `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`。

```python
def subsets(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int) -> None:
        res.append(path[:])                 # 每个节点都是一个子集：进来先记一份快照
        for i in range(start, len(nums)):   # 只往后选，保证同一个子集不会按不同顺序出现两次
            path.append(nums[i])
            dfs(i + 1)
            path.pop()                      # 回溯：撤销选择

    dfs(0)
    return res
```
