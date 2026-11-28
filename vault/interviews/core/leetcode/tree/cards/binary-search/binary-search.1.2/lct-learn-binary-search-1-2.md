---
id: lct-learn-binary-search-1-2
node: binary-search.1.2
type: qa
step: 1
---
## Q
**二分算法 › 二分查找 › 进阶**｜学习卡

套路是什么？

## A
**一句话。** 进阶题先造出有序数组（排序、按时间追加、把二维拍平），再把条件移项成“元素 `>=` 某个阈值”，答案就是 `lower_bound` 的下标。

下图：LC 2300，排序后把条件移项成「`p >=` 阈值」，满足的是一个后缀。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="70" y="50" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="110" y="50" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="150" y="50" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="190" y="50" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="210.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="230" y="50" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="250.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="14" y="70" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">potions</text>
<line x1="150" y1="44" x2="150" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="270" y1="44" x2="270" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="150" y1="44" x2="270" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="210.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≥ 阈值的后缀：m - lb = 3 个</text>
<line x1="170.0" y1="96" x2="170.0" y2="82" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,82.0 173.0,88.3 167.0,88.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">lb</text>
<text x="170" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">s·p ≥ 7 ⇔ p ≥ ⌈7/3⌉ = 3（spell = 3）</text>
</svg>

```python
def lower_bound(a, x):              # 第一个 >= x 的下标
    left, right = -1, len(a)
    while left + 1 < right:
        mid = (left + right) // 2
        if a[mid] >= x:
            right = mid
        else:
            left = mid
    return right


def successful_pairs(spells, potions, success):  # LC 2300
    potions.sort()                  # 先排序，才能二分
    m = len(potions)
    # s * p >= success 的最小 p，上取整；>= 阈值的个数 m - lb
    return [m - lower_bound(potions, (success + s - 1) // s)
            for s in spells]
```

**要点。**
- 为什么对？：排序后“`s * p >= success`”对 `p` 单调，满足的药水构成一个后缀，后缀长度就是 `m - lb`。
- LC 981、LC 1146 怎么改？：每个 key（下标）存一个追加的 `(时间戳 / 快照号, 值)` 列表，`get` 找最后一个 `<= t` 的记录，即 `lb(t+1) - 1`，下标 `-1` 表示没有。
- LC 74 搜索二维矩阵怎么改？：整个矩阵当长度 `m·n` 的有序数组，`mid` 拆成 `(mid // n, mid % n)`，`n` 是列数。
- LC 658 找到 K 个最接近的元素怎么改？：二分窗口起点 `(−1, n−k)`，若 `x - arr[mid] > arr[mid+k] - x` 则起点右移。

**易错点。**
- 阈值下取整：`spells = [5]`、`potions = [1,2]`、`success = 7` 应得 `[1]`，用 `success // s` 会得到 `[2]`。
- 没有更早的记录：981 先 `set("a","x",5)`，`get("a",3)` 应为 `""`，`lb(4) - 1 = -1`，`list[-1]` 会取到最后一条。
- 658 右端取 `n`：`arr = [1,2,3]`、`k = 2`、`x = 3` 应得 `[2,3]`，右端要是 `n - k`，否则越界。

**对应题目。** LC 658 找到 K 个最接近的元素、LC 1385 两个数组间的距离值、LC 74 搜索二维矩阵、LC 1146 快照数组、LC 2300 咒语和药水的成功对数、LC 981 基于时间的键值存储
