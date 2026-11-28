---
id: lct-learn-data-structures-5-3
node: data-structures.5.3
type: qa
step: 1
---
## Q
**常用数据结构 › 堆（优先队列） › 第 K 小/大**｜学习卡

套路是什么？

## A
**一句话。** 前 `k` 个最小元素不需要全排序：把若干条升序序列的「当前头」放进小根堆，每弹出一个最小值，就把它所在序列的下一个补进来，弹 `k` 次即得。

下图：每行是一条升序序列，堆里只放各行的当前头；弹出一个就补同一行的下一个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<text x="20" y="22" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a[i] + b[j]（a = 1,7,11；b = 2,4,6）</text>
<text x="24" y="53" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i=0</text>
<rect x="44" y="34" width="40" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="64" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="84" y="34" width="40" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="104" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="124" y="34" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="144" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7</text>
<text x="24" y="89" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i=1</text>
<rect x="44" y="70" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="64" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">9</text>
<rect x="84" y="70" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="104" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">11</text>
<rect x="124" y="70" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="144" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">13</text>
<text x="24" y="125" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i=2</text>
<rect x="44" y="106" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="64" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">13</text>
<rect x="84" y="106" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="104" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15</text>
<rect x="124" y="106" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="144" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">17</text>
<text x="104" y="158" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每行自身升序；虚线 = 已弹出</text>
<rect x="210" y="60" width="110" height="56" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="265" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆：每行当前头</text>
<text x="265" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7  9  13</text>
<line x1="168" y1="48" x2="208" y2="70" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="208.0,70.0 201.0,69.6 203.9,64.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="265" y="136" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">弹 5 后补同行的 7</text>
</svg>

```python
def k_smallest_pairs(a, b, k):       # a、b 升序，求和最小的 k 对
    # 序列 i：a[i] + b[0], a[i] + b[1], ... 本身升序
    h = [(a[i] + b[0], i, 0) for i in range(min(k, len(a)))]
    heapify(h)                       # 前 k 个 a 足够，其余必然更大
    res = []
    while h and len(res) < k:
        _, i, j = heappop(h)         # 当前最小的一对
        res.append([a[i], b[j]])
        if j + 1 < len(b):           # 同一序列的下一个进堆
            heappush(h, (a[i] + b[j + 1], i, j + 1))
    return res
```

**要点。**
- 为什么对？：每条序列内部升序，堆里始终有每条序列的最小未取元素，所以堆顶就是全局最小未取元素；`O(k log k)`，不用生成 `m * n` 对。
- 第 K 大数怎么改？：维护大小为 `k` 的小根堆，新元素比堆顶大就替换，最后堆顶就是第 `k` 大。
- 有序矩阵第 K 小怎么改？：每行是一条升序序列，初始放每行（或前 `k` 行）的第一个元素，同样弹 `k` 次。

**易错点。**
- 初始放全部 `m * n` 对：会爆时间和内存，只放每条序列的头。
- 序列长度不足：`j + 1 < len(b)` 要判断，否则越界。
- 求第 K 大却用大根堆装全部元素：`O(n log n)`，用大小为 `k` 的小根堆才是 `O(n log k)`。

**对应题目。** LC 373 查找和最小的 K 对数字
