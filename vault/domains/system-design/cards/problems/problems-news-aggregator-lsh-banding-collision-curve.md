---
id: problems-news-aggregator-lsh-banding-collision-curve
node: problems.search.news-aggregator
type: qa
step: 3
tags: [grown]
---
## Q
In an LSH banding scheme for MinHash-based near-duplicate detection, splitting a 128-value signature into b=16 bands of r=8 rows each, why does the candidate-pair probability form a sharp S-curve as true Jaccard similarity increases, rather than a straight line?

## A
A pair becomes a candidate if it matches exactly on at least one band, and the probability of matching within any single band is s^r (all r rows in that band must agree), so the probability of NOT matching any of the b bands is (1-s^r)^b, making the candidate probability 1-(1-s^r)^b. Because this formula raises s to the r-th power before the b-th power is applied, low-similarity pairs are suppressed multiplicatively across two exponents, producing a steep transition rather than a gradual one. Computed for b=16, r=8: at s=0.5 the candidate probability is about 6.1% (weakly similar pairs are filtered out), at s=0.65 about 40.4%, at s=0.8 about 94.7% (near-duplicates are almost always recalled), with the 50% crossover near s≈0.67.

## Q zh
在一个基于 MinHash 的近似重复检测 LSH banding 方案中，把 128 维签名切成 b=16 个宽度 r=8 的 band，为什么候选对概率随真实 Jaccard 相似度增加会形成一条陡峭的 S 型曲线，而不是一条直线？

## A zh
一对文档只要在至少一个 band 上完全匹配就成为候选对，而在任意一个 band 内完全匹配的概率是 s^r（该 band 内全部 r 行都要一致），所以在全部 b 个 band 上都不匹配的概率是 `(1-s^r)^b`，候选概率因此是 `1-(1-s^r)^b`。因为这个公式先把 s 取 r 次方，再对结果取 b 次方，低相似度的对会在两层指数上被同时压低，产生陡峭而不是渐变的过渡。以 b=16、r=8 计算：s=0.5 时候选概率约 6.1%（弱相似对被过滤），s=0.65 时约 40.4%，s=0.8 时约 94.7%（真正的近似重复几乎都被召回），50% 临界点在 s≈0.67 附近。
