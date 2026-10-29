---
id: uth-go-rust-go-slice-map-3-swiss
node: go-rust.go-slice-map
type: qa
step: 3
---
## Q
**Go 的 map 现在是什么结构**｜Go · 1.24 起

Go 1.24 换了新的 `map` 实现，查找为什么更快？

## A
**背景。** 哈希表把 key 算成一个数，用它当位置。两个 key 算到同一个位置（冲突）时有两种办法：挂链，或者去别的槽里找空位（开放寻址）。老 map 用桶加链；1.24 起改用开放寻址，把槽分成一组一组，一次比对一整组。

**结构。** 瑞士表（Swiss table）：每 8 个槽一组，带一个 8 字节控制字；开放寻址，组间二次探测。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Go 1.24: 目录 → 若干张小表 → 每组 8 槽</text>
<rect x="10" y="26" width="100" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="60" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">目录 (directory)</text>
<line x1="110" y1="38" x2="150" y2="40" stroke="currentColor" stroke-width="1"/>
<polygon points="150,40 143.9,42.4 144.1,37.0" fill="currentColor"/>
<rect x="150" y="26" width="180" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="158" y="40" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">表 1 (最多 1024 槽)</text>
<rect x="158" y="46" width="78" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="197" y="60.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">控制字 + 8 槽</text>
<rect x="242" y="46" width="78" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="281" y="60.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">控制字 + 8 槽</text>
<line x1="110" y1="38" x2="150" y2="106" stroke="currentColor" stroke-width="1"/>
<polygon points="150,106 144.6,102.2 149.3,99.5" fill="currentColor"/>
<rect x="150" y="96" width="180" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="158" y="106" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">表 2 (最多 1024 槽)</text>
<rect x="158" y="112" width="78" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="197" y="126.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">控制字 + 8 槽</text>
<rect x="242" y="112" width="78" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="281" y="126.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">控制字 + 8 槽</text>
<text x="8" y="170" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">控制字每字节 = 槽状态 + 哈希低 7 位, 一次比对 8 槽</text>
<text x="8" y="188" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只扩容一张小表, 不会整个 map 一次性重新哈希</text>
</svg>
```

**细节。**

- 控制字每字节存槽状态和哈希的低 7 位，一次位运算同时比对 8 个槽
- 负载因子 7/8（装到 7/8 满就扩容）
- 单张表最多 1024 个槽，再大就拆成两张表（可扩展哈希，extendible hashing：用一层目录指向多张小表）

**为什么。** 一次只扩容一张小表，不会整个 map 一次性重新哈希，延迟抖动小；组内并行比较。

**坑。** 遍历顺序不保证，运行时还会随机化起点，不要依赖。

**例题：** LC 1 两数之和（同类：LC 146 LRU 缓存）

给整数数组 `nums` 和目标值 `target`，返回和为 `target` 的两个元素的下标，同一个元素不能用两次。例：`[2,7,11,15]`、`target = 9` → `[0,1]`。Go 的 `map` 在这里的作用：一趟扫描，用值直接查到下标。

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}  # 值 -> 下标，只含已扫过的左半段
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:
            return [j, i]
        seen[x] = i
    return []
```
