---
id: uth-go-rust-go-slice-map-2-alias
node: go-rust.go-slice-map
type: qa
step: 2
---
## Q
**对子切片 append 为什么改了原数组**｜Go · slice

`b := a[:2]; b = append(b, 99)` 之后，为什么 `a` 变成了 `[1 2 99 4]`？

## A
**背景。** 切片只是窗口，不拥有数据。`a[:2]` 没有复制任何元素，只是换了一扇更窄的窗口，背后还是同一个数组。往这扇窗口里 `append`，如果容量够，就直接写进共享的数组。

**结构。** 子切片和原切片共用同一个底层数组，只是长度、容量不同。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 185">
<text x="8" y="14" text-anchor="start" font-size="11" font-family="sans-serif" font-weight="bold" fill="currentColor">a := []int{1,2,3,4}; b := a[:2]; b = append(b, 99)</text>
<rect x="40" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="65" y="58.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="96" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="121" y="58.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="152" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="177" y="58.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">99</text>
<rect x="208" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="233" y="58.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="8" y="58" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">底层</text>
<line x1="40" y1="82" x2="150" y2="82" stroke="currentColor" stroke-width="1"/>
<polygon points="150,82 144.0,84.7 144.0,79.3" fill="currentColor"/>
<polygon points="40,82 46.0,79.3 46.0,84.7" fill="currentColor"/>
<text x="95" y="98" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">b: len 2</text>
<line x1="40" y1="112" x2="262" y2="112" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="262,112 256.0,114.7 256.0,109.3" style="fill:var(--accent,#3b6fd4)"/>
<polygon points="40,112 46.0,109.3 46.0,114.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="150" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">b: cap 4, 容量够, 直接写第 3 格</text>
<text x="8" y="156" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">a 与 b 共用同一个底层数组, 所以 a 变成 [1 2 99 4]</text>
<text x="8" y="174" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a[:2:2] 把容量也限成 2, 下次 append 就复制到新数组</text>
</svg>
```

**细节。**

- `a` 是 `[1 2 3 4]`，`b := a[:2]` 的容量仍是 4
- 容量够，`append` 直接写进共享数组的第 3 格
- 实测输出：`a = [1 2 99 4]`，`b = [1 2 99]`，`cap(b) = 4`
- 用 `a[:2:2]` 把容量也限定为 2，下一次 `append` 就会复制到新数组

**为什么。** 切片是不拷贝数据的廉价视图，代价是别名要自己管。

**坑。** 回溯里保存路径要 `append([]int(nil), path...)` 拷贝，否则会被后续修改改坏。

**例题：** LC 78 子集（同类：LC 39 组合总和）

给元素互不相同的整数数组，返回它所有的子集（不能重复）。例：`[1,2,3]` → `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`。回溯时用同一个 `path` 列表，所以收集结果必须拷一份 `path[:]`，否则之后的修改会改坏已经收集的答案。

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
