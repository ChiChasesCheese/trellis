---
slug: ugly-number-ii
---
## Q
**LC 264 丑数 II**｜Medium

质因子只含 2、3、5 的正整数叫丑数（1 也算），求第 `n` 个丑数（`n <= 1690`）。

## A
**一句话。** 每个丑数都是更小的丑数乘 2、3 或 5，相当于三条有序链 `f×2`、`f×3`、`f×5` 的多路归并；三个指针各指向下一个要乘的位置，每次取最小，相等的指针一起前移去重。

**图解。** 已得到 `1..8` 七个丑数，三个指针给出候选 `10、9、10`，下一个是 9，只移动 `p3`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 126">
<text x="27" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f</text>
<rect x="35" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="65" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="95" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="125" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="155" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="185" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="215" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="245" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">?</text>
<text x="80.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">p5</text>
<text x="110.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">p3</text>
<text x="170.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">p2</text>
<text x="16" y="90" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">候选：5×2 = 10，3×3 = 9，2×5 = 10</text>
<text x="16" y="108" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">取最小 9，只有 p3 前移</text>
</svg>

```python
def nth_ugly_number(n):
    f = [1] * n
    p2 = p3 = p5 = 0           # 下一个要乘 2、3、5 的位置
    for i in range(1, n):
        a, b, c = f[p2] * 2, f[p3] * 3, f[p5] * 5
        f[i] = min(a, b, c)
        if f[i] == a:          # 三个 if 都要判：相等就一起走
            p2 += 1
        if f[i] == b:
            p3 += 1
        if f[i] == c:
            p5 += 1
    return f[-1]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `elif`：`6 = 2×3 = 3×2` 时只移一个指针，下一轮会再生成一个 6。
- 从 1 往上逐个判断是不是丑数：第 1690 个丑数约 `2·10^9`，太慢。

**追问。**
- 用堆？：最小堆从 1 开始，每弹出 `x` 就压入 `2x、3x、5x`，用集合去重，`O(n log n)`。
- 质因子集合任意给定？：同样每个质数一个指针，就是 LC 313。

**同模式。** LC 23 合并 K 个升序链表、LC 313 超级丑数、LC 373 查找和最小的 K 对数字
