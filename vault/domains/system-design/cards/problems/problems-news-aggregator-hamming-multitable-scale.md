---
id: problems-news-aggregator-hamming-multitable-scale
node: problems.search.news-aggregator
type: qa
step: 4
tags: [grown]
---
## Q
In a news aggregator using 64-bit SimHash fingerprints with a Hamming-distance threshold of k=3 for near-duplicate detection, how does the multi-table permutation technique (splitting the fingerprint into blocks, building one sorted table per choice of blocks) let the number of tables be tuned to the size of the active corpus, and what design works for a 7.2-million-article active window?

## A
Each table is built by permuting fingerprints so a chosen subset of blocks (totaling p_i bits) becomes the leading bits, then sorting; a probe for a query fingerprint retrieves on average 2^d × 2^-p_i matching (permuted) fingerprints, where d = log2(corpus size). Larger p_i (more leading bits per table) means fewer candidates per probe but requires more tables to guarantee covering every possible k-bit-position combination. For a 7.2-million-article active window (d ≈ 22.78), splitting the 64-bit fingerprint into 6 blocks of about 11 bits and choosing 2 of the 6 blocks per table gives C(6,2) = 15 tables with p_i ≈ 22, yielding about 1.7 candidate fingerprints per probe on average — fewer tables than a design built for a much larger corpus would need to hit a similar candidates-per-probe target.

## Q zh
在一个用 64 位 SimHash 指纹、汉明距离阈值 k=3 做近似重复检测的新闻聚合器中，多表置换技术（把指纹切成若干块，为每种块的选择方式建一张排序表）如何让表的数量能按活跃语料规模调节？对一个 720 万篇文章的活跃窗口，什么设计是合适的？

## A zh
每张表通过把指纹按某个选定的块子集（共 p_i 位）置换成前导位再排序来构建；对一个查询指纹的一次探测平均会返回 `2^d × 2^-p_i` 个匹配的（置换后）指纹，其中 d = log2(语料规模)。p_i 越大（每张表的前导位越多）每次探测的候选数越少，但需要更多张表才能覆盖所有可能的 k 位差异组合。对一个 720 万篇文章的活跃窗口（d ≈ 22.78），把 64 位指纹切成 6 个约 11 位的块、每张表选其中 2 块，得到 `C(6,2) = 15` 张表、`p_i ≈ 22`，平均每次探测约 1.7 个候选指纹——比为规模大得多的语料设计的方案所需的表数要少，却能达到类似的候选数目标。
