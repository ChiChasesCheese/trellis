---
id: lct-learn-binary-search-2-1
node: binary-search.2.1
type: qa
step: 1
---
## Q
**二分算法 › 二分答案 › 求最小**｜学习卡

套路是什么？

## A
**一句话。** 求最小的可行答案：把答案范围想成虚拟数组 `check(lo..hi) = 假…假真…真`，用 `lower_bound` 的写法找第一个真，`check` 通常是一次 `O(n)` 的贪心。

下图：LC 875（piles = [3,6,7,11]，h = 8），答案范围是一个虚拟的有序数组。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="50" width="25" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="32.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">F</text>
<rect x="45" y="50" width="25" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">F</text>
<rect x="70" y="50" width="25" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="82.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">F</text>
<rect x="95" y="50" width="25" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="107.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">F</text>
<rect x="120" y="50" width="25" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="132.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">T</text>
<rect x="145" y="50" width="25" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="157.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">T</text>
<rect x="170" y="50" width="25" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="182.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">T</text>
<rect x="195" y="50" width="25" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="207.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">T</text>
<rect x="220" y="50" width="25" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="232.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">T</text>
<rect x="245" y="50" width="25" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="257.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">T</text>
<rect x="270" y="50" width="25" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="282.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">T</text>
<rect x="295" y="50" width="25" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="307.5" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">T</text>
<text x="32.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="57.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="82.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="107.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="132.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="157.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="182.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<text x="207.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<text x="232.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<text x="257.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<text x="282.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<text x="307.5" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">11</text>
<text x="20" y="40" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">v = 速度：check(v)</text>
<line x1="132.5" y1="114" x2="132.5" y2="100" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="132.5,100.0 135.5,106.3 129.5,106.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132.5" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">答案 4</text>
<text x="170" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">假…假真…真：用 lower_bound 找第一个真</text>
</svg>

```python
def binary_min(left, right, check):
    # 不变量：check(left) 为假，check(right) 为真
    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            right = mid             # mid 可行，答案在 (left, mid]
        else:
            left = mid
    return right                    # 最小的可行值


def min_eating_speed(piles, h):     # LC 875
    def check(v):                   # 速度 v 能否在 h 小时内吃完
        return sum((p + v - 1) // v for p in piles) <= h
    return binary_min(0, max(piles), check)
```

**要点。**
- 为什么对？：`check` 单调（速度越快越可行），所以虚拟数组是 `假…假真…真`；`left` 是一定不可行的值，`right` 是一定可行的值，两个端点不会被 `check` 调用。
- LC 1011 送包裹的能力、LC 1482 做花束怎么改？：只换 `check`。1011 贪心装包，装不下就开新的一天，`left = max(weights) - 1`；1482 数连续开花段能凑几束，先排除 `m·k` 超过花数的情形。
- LC 475 供暖器怎么改？：`check(r)` 判断半径 `r` 能否覆盖所有房子，房子与供暖器都排序后双指针。

**易错点。**
- 上界取小了：`piles = [1]`、`h = 1`，`right = max - 1 = 0` 会返回 `0`，应为 `1`。
- 上取整写成下取整：`piles = [3,6,7,11]`、`h = 8` 应得 `4`，`p // v` 会低估耗时。
- 1011 不拦超重包裹：`weights = [1,10]`、`days = 2` 应得 `10`，`left` 要从 `max(weights) - 1` 起。

**对应题目。** LC 1011 在 D 天内送达包裹的能力、LC 475 供暖器、LC 875 爱吃香蕉的珂珂、LC 1482 制作 m 束花所需的最少天数
