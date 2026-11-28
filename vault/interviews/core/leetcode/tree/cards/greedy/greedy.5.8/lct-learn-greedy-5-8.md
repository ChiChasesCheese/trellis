---
id: lct-learn-greedy-5-8
node: greedy.5.8
type: qa
step: 1
---
## Q
**贪心算法 › 思维题 › 分类讨论**｜学习卡

套路是什么？

## A
**一句话。** 分类讨论：先把所有情形按结构分成有限几类，每类算一个闭式代价，再取小或求和。

下图：LC 1247，所有情形只分成几类，每类一个闭式代价。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<rect x="84.6" y="7.5" width="170.8" height="25" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只看不同的位置：数 xy、yx</text>
<polygon points="110.2,66.0 119.2,53.5 220.8,53.5 229.8,66.0 220.8,78.5 119.2,78.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="70.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xy + yx 是奇数？</text>
<rect x="278.0" y="53.5" width="44" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="300" y="70.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="29.2" y="102.0" width="121.6" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同类一对</text>
<text x="90" y="133.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xy + xy：换 1 次</text>
<rect x="189.2" y="102.0" width="121.6" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">剩一对异类</text>
<text x="250" y="133.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xy + yx：换 2 次</text>
<rect x="78.5" y="169.5" width="183.0" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="186.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">xy//2 + yx//2 + 2·(xy%2)</text>
<path d="M 170.0 32.5 L 170.0 53.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,53.5 167.0,47.2 173.0,47.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 229.8 66.0 L 278.0 66.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="278.0,66.0 271.7,69.0 271.7,63.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="262" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 170.0 78.5 L 170.0 94.0 L 90.0 94.0 L 90.0 102.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,102.0 87.0,95.7 93.0,95.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="90" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 170.0 78.5 L 170.0 94.0 L 250.0 94.0 L 250.0 102.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,102.0 247.0,95.7 253.0,95.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 90.0 142.0 L 90.0 160.0 L 150.0 160.0 L 170.0 169.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,169.5 163.0,169.5 165.6,164.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 250.0 142.0 L 250.0 160.0 L 190.0 160.0 L 170.0 169.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,169.5 174.4,164.1 177.0,169.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>

```python
def minimum_swap(s1, s2):        # LC 1247：只看两串不同的位置
    xy = yx = 0                  # xy：s1 是 x 而 s2 是 y 的位置数
    for a, b in zip(s1, s2):
        if a != b:
            if a == "x":
                xy += 1
            else:
                yx += 1
    if (xy + yx) % 2:            # 不同位置为奇数：无解
        return -1
    # 同类两个换 1 次；剩一对异类要 2 次
    return xy // 2 + yx // 2 + 2 * (xy % 2)
```

**要点。**
- 为什么对？：相同位置不用动；不同位置只有 `xy`、`yx` 两类，同类两个一次交换解决，一对异类要先转成同类再换，共两次。
- LC 3942 怎么改？：只有循环升序或循环降序的排列能排好；按 `0` 的位置 `p` 分别算「左旋 `p` 次」「反转后左旋」等几种代价取小，都不成立返回 `-1`。
- LC 2468 怎么改？：枚举总段数 `b`，后缀长度由 `b` 的位数定；总容量 `b * (limit - 后缀) - 编号位数和 >= n` 的最小 `b` 就是段数，再按固定后缀从左到右切。

**易错点。**
- LC 1247 答案写成不同位置数的一半：`("xy", "yx")` 得 `1`，应为 `2`。
- LC 3942 忘了循环降序也能排好：`[0,2,1]` 得 `-1`，应为 `2`。
- LC 2468 所有编号按一位数估容量：编号 `10` 起是两位数，容量会算多。

**对应题目。** LC 1247 交换字符使得字符串相同、LC 3942 排序排列的最少操作数、LC 2468 根据限制分割消息
