---
id: lct-learn-data-structures-7-6
node: data-structures.7.6
type: qa
step: 1
---
## Q
**常用数据结构 › 并查集 › 带权并查集（边权并查集）**｜学习卡

套路是什么？

## A
**一句话。** 带权并查集：每个点记 `w[x] = x / 父`，路径压缩时把比值累乘到根；同根的两点之比由各自到根的比值相除得到。

下图：路径压缩时把沿途的比值乘到根；同根两点之比 = 各自到根的比值相除。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="80" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">压缩前</text>
<circle cx="80" cy="45" r="14" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">r</text>
<circle cx="80" cy="105" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<circle cx="80" cy="165" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="80" y1="151" x2="80" y2="120" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,120.0 83.0,126.3 77.0,126.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="90" y="140" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">w[a] = a/b = 2</text>
<line x1="80" y1="91" x2="80" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,60.0 83.0,66.3 77.0,66.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="90" y="80" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">w[b] = b/r = 3</text>
<text x="255" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">find(a) 后</text>
<circle cx="255" cy="45" r="14" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="255" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">r</text>
<circle cx="205" cy="110" r="14" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="205" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="215.0" y1="96" x2="242.5" y2="58" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="242.5,58.0 241.2,64.9 236.4,61.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<circle cx="255" cy="110" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<line x1="255.0" y1="96" x2="255.0" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,58.0 258.0,64.3 252.0,64.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<circle cx="305" cy="110" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="305" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<line x1="295.0" y1="96" x2="267.5" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="267.5,58.0 273.6,61.4 268.8,64.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="205" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2·3 = 6</text>
<text x="255" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<text x="305" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1.5</text>
<text x="255" y="170" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a / c = w[a] / w[c] = 6 / 1.5 = 4</text>
</svg>

```python
p, w = list(range(n)), [1.0] * n   # w[x] = x / p[x]

def find(x):                     # 返回根，并压成 w[x] = x / 根
    if p[x] != x:
        root = find(p[x])
        w[x] *= w[p[x]]          # 此时 w[p[x]] = p[x] / 根
        p[x] = root
    return p[x]

def union(a, b, v):              # 已知 a / b = v
    ra, rb = find(a), find(b)
    if ra != rb:
        p[ra] = rb
        w[ra] = v * w[b] / w[a]  # 公式见要点

def query(a, b):                 # 同根时 a / b = w[a] / w[b]
    if find(a) != find(b):
        return -1.0
    return w[a] / w[b]
```

**要点。**
- 为什么对？：`w[x]` 是 `x / 父`，沿父链累乘到根就是 `x / 根`；同根两点的根相同，相除后根约掉，得到 `a / b`。
- 合并公式怎么来？：把 `ra` 挂到 `rb` 下，需要 `ra / rb`：它等于 `(a / b) * (b / rb) / (a / ra) = v * w[b] / w[a]`，所以必须先 `find` 两端，让 `w` 都是对根的比值。
- 边权是差或异或怎么改？：累乘改累加（或异或），`w[x] = x - 父`，合并 `w[ra] = v + w[b] - w[a]`（`a - b = v`）；异或版把加减都换成异或。

**易错点。**
- 没先 `find` 就合并：`w[a]`、`w[b]` 还不是对根的比值，合并出来的权错。
- 查询的变量没出现过：不在表里直接返回 `-1.0`，`a / a` 也一样（`a` 不存在时）。

**对应题目。** LC 399 除法求值
