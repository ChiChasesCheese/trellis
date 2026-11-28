---
id: lct-learn-binary-search-2-6
node: binary-search.2.6
type: qa
step: 1
---
## Q
**二分算法 › 二分答案 › 第 K 小/大**｜学习卡

套路是什么？

## A
**一句话。** 第 `k` 小 = 最小的 `x` 使 `<= x` 的数至少有 `k` 个：二分答案求最小，`check` 是“数个数”，只要能在 `O(n)` 里数出不超过 `x` 的个数，就不必展开 `n²` 个候选。

下图：LC 378，二分答案 `x`，用阶梯走法 `O(n)` 数出不超过 `x` 的个数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 145">
<rect x="20" y="20" width="44" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="42" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="64" y="20" width="44" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="86" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
<rect x="108" y="20" width="44" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="130" y="41" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">9</text>
<rect x="20" y="54" width="44" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="42" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">10</text>
<rect x="64" y="54" width="44" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="86" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">11</text>
<rect x="108" y="54" width="44" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="130" y="75" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">13</text>
<rect x="20" y="88" width="44" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="42" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">12</text>
<rect x="64" y="88" width="44" height="34" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="86" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">13</text>
<rect x="108" y="88" width="44" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">15</text>
<line x1="50" y1="105" x2="76" y2="105" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="76.0,105.0 69.7,108.0 69.7,102.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="94" y1="105" x2="120" y2="105" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,105.0 113.7,108.0 113.7,102.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="130" y1="97" x2="130" y2="81" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="130.0,81.0 133.0,87.3 127.0,87.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="175" y="34" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">x = 13：数 ≤ x 的个数</text>
<text x="175" y="52" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">从左下角走阶梯</text>
<text x="175" y="68" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">≤ x：本列上面都算，右移</text>
<text x="175" y="84" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">&gt; x：上移</text>
<text x="175" y="106" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">count = 8 ≥ k</text>
<text x="170" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">二分最小的 x 使 count(x) ≥ k；不必展开 n² 个数</text>
</svg>

```python
def kth_smallest(matrix, k):        # LC 378：行列都递增
    n = len(matrix)
    def count_le(x):                # 阶梯走法数 <= x 的个数
        i, j, cnt = n - 1, 0, 0     # 左下角出发
        while i >= 0 and j < n:
            if matrix[i][j] <= x:
                cnt += i + 1        # 这一列到第 i 行都 <= x
                j += 1
            else:
                i -= 1
        return cnt
    left, right = matrix[0][0] - 1, matrix[-1][-1]
    while left + 1 < right:         # 最小的 x 使计数 >= k
        mid = (left + right) // 2
        if count_le(mid) >= k:
            right = mid
        else:
            left = mid
    return right
```

**要点。**
- 为什么对？：`count_le` 随 `x` 单调不减；最小的 `x` 使 `count_le(x) >= k` 一定是矩阵里的某个元素，因为 `x` 取不到元素时计数不变。
- LC 719 第 K 小的距离对怎么改？：先排序，二分距离 `d`，`count_le` 用双指针：每个右端 `j` 把左端 `i` 追到 `v - nums[i] <= d`，贡献 `j - i`。
- LC 1918 第 K 小的子数组和怎么改？：元素为正，二分和 `s`，用滑动窗口数和 `<= s` 的子数组，每个右端点贡献窗口长度。
- LC 793 阶乘后 K 个零怎么改？：`f(x) = x//5 + x//25 + …` 单调，答案是 `lb(k+1) - lb(k)`（`lb(v)` 为最小的 `x` 使 `f(x) >= v`），只会是 `0` 或 `5`。

**易错点。**
- 判定写成 `count_le(mid) > k`：`matrix = [[1,2],[1,3]]`、`k = 2` 应得 `1`，会得到 `2`。
- 值域下界写错：719 `nums = [1,6,1]`、`k = 1` 应得 `0`，`left` 要是 `lo - 1 = -1`，写成 `0` 会得到 `1`。
- 719 忘了先排序：`nums = [3,1]` 的计数会错。

**对应题目。** LC 719 找出第 k 小的距离对、LC 378 有序矩阵中第 K 小的元素、LC 1918 第 K 小的子数组和、LC 793 阶乘函数后 K 个零
