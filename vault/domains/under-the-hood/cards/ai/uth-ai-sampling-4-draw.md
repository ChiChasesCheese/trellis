---
id: uth-ai-sampling-4-draw
node: ai.sampling
type: qa
step: 4
---
## Q
**按概率抽出一个词**｜llama.cpp · vLLM

留下的词各有一个概率，手里只有「0 到 1 之间均匀的随机数」。怎样按概率抽出一个词？

## A
**背景。** 要让概率 0.5 的词有一半机会被抽中，得把「均匀」换成「按概率」。想象长度为 1 的线段，每个词占一段，长度就是概率；扔一个点，落在谁的段里就选谁。

**结构。** 前缀和（prefix sum）加扫描：随机数 `r` 乘以概率总和得到目标值，从头累加每个词的概率，第一次累加到不小于目标就停，停在谁就选谁。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="20" y="56" width="193.2" height="26" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="116.6" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">好</text>
<rect x="213.2" y="56" width="71.1" height="26" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="248.8" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">热</text>
<rect x="284.3" y="56" width="26.1" height="26" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="297.4" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冷</text>
<rect x="310.4" y="56" width="9.6" height="26" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="315.2" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">差</text>
<text x="20" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="213.2" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0.64</text>
<text x="284.3" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0.88</text>
<text x="320" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<line x1="260" y1="26" x2="260" y2="56" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="260,56 257,49 263,49" style="fill:var(--accent,#3b6fd4)"/>
<text x="260" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">r = 0.80</text>
<text x="170" y="136" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个词占一段, 长度就是概率; 扔个点, 落在谁的段里选谁</text>
</svg>
```

**细节。**

- llama.cpp 就是这样：一遍扫描里完成累加、定位和归一化
- 每次 O(词数)；反复抽同一个分布时，可先算好前缀和再二分，O(log n)
- vLLM 在 GPU 上换了办法：给每个词配一个指数分布 `Exp(1)` 的随机数 `q`，选 `概率 / q` 最大的词，结果恰好服从原来的概率分布，一次并行的 `argmax` 就完成

**为什么。** 源码注释写明不用 `torch.multinomial`，因为它会让 CPU 和 GPU 互相等待（同步）；`argmax` 不需要。

**例题：** LC 528 按权重随机选择

给正整数数组 `w`，`w[i]` 是下标 `i` 的权重；`pickIndex()` 要以 `w[i] / sum(w)` 的概率返回 `i`。例：`w = [1, 3]` 时，下标 `0` 的概率是 25%，下标 `1` 是 75%。

```python
import random
from bisect import bisect_right
from itertools import accumulate


class Solution:
    def __init__(self, w: list[int]):
        self.prefix = list(accumulate(w))        # prefix[i] = w[0] + ... + w[i]
        self.total = self.prefix[-1]

    def pickIndex(self) -> int:
        r = random.randrange(self.total)         # 均匀落在 [0, total)
        return bisect_right(self.prefix, r)      # 第一个 prefix[i] > r 的 i
```
