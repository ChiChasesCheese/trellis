---
id: lct-learn-math-5-3
node: math.5.3
type: qa
step: 1
---
## Q
**数学算法 › 计算几何 › 矩形、多边形**｜学习卡

套路是什么？

## A
**一句话。** 矩形题把几何化成坐标比较：重叠宽高各是 `min(右) - max(左)`，负数按 `0`；找矩形把点放进哈希集合，枚举对角线，另外两角查表。

下图：两矩形的重叠部分，宽高各是「较小的右边减较大的左边」。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="30" y="40" width="140" height="80" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="110" y="70" width="140" height="70" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="110" y="70" width="60" height="50" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<line x1="110" y1="32" x2="110" y2="26" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="170" y1="32" x2="170" y2="26" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="110" y1="32" x2="170" y2="32" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="140.0" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">w = min(右) - max(左)</text>
<text x="176" y="98" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">h</text>
<text x="40" y="58" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A</text>
<text x="238" y="134" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">B</text>
<text x="262" y="64" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">面积 = A + B</text>
<text x="262" y="80" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">  - 重叠 w·h</text>
<text x="262" y="104" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">w 或 h 为负</text>
<text x="262" y="120" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按 0 算</text>
<text x="170" y="156" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">找矩形：点进集合，枚举对角线两点，另两角查表</text>
</svg>

```python
def compute_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    w = max(0, min(ax2, bx2) - max(ax1, bx1))   # 重叠宽
    h = max(0, min(ay2, by2) - max(ay1, by1))   # 重叠高
    return area_a + area_b - w * h              # 容斥

def min_area_rect(points):           # 点集里轴对齐矩形
    seen = {tuple(p) for p in points}
    best = float("inf")
    for x1, y1 in seen:
        for x2, y2 in seen:          # 左下、右上当对角线
            if x1 < x2 and y1 < y2:
                if (x1, y2) in seen and (x2, y1) in seen:
                    best = min(best, (x2 - x1) * (y2 - y1))
    return 0 if best == float("inf") else best
```

**要点。**
- 为什么对？：轴对齐矩形由一条对角线唯一确定另外两角，只枚举左下、右上这一种对角线，每个矩形恰好数一次。
- LC 593 怎么改？：四点的 6 个两两平方距离排序，必须是 `[s, s, s, s, 2s, 2s]` 且 `s > 0`。

**易错点。**
- 不相交时宽高都是负数，相乘变正：漏掉 `max(0, ·)`，`(0,0,1,1)` 与 `(2,2,3,3)` 得 `1`，应为 `2`。
- LC 593 漏掉 `s > 0`：四点重合时 6 个距离全是 `0`，会错判 `True`。
- LC 593 只查四条边相等：菱形 `[0,0],[2,9],[9,2],[11,11]` 四边相等，对角线不等，应为 `False`。

**对应题目。** LC 223 矩形面积、LC 593 有效的正方形、LC 939 最小面积矩形
