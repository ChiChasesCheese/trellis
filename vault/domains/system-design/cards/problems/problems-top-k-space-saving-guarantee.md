---
id: problems-top-k-space-saving-guarantee
node: problems.search.top-k
type: qa
step: 4
tags: [grown]
---
## Q
State the Space-Saving algorithm's deterministic guarantee (Metwally, Agrawal & El Abbadi's Theorem 3) for finding Top-K candidates in a stream, and compute how many counters `m` are needed to guarantee capturing every item with at least 500,000 views out of a 60-billion-event daily window.

## A
Space-Saving keeps only `m` counters: on a new, unmonitored element it evicts the currently-smallest counter and gives the new element that counter's value + 1. Theorem 3's guarantee, with no assumption about data distribution: as long as `m ≥ 1/ε`, any element whose true frequency `f_i > ε*N` is guaranteed to be present in the final monitored set — this is a zero-false-negative guarantee, not a probabilistic one. To guarantee capturing every item with ≥500,000 daily views out of N=6e10: `ε = 500,000 / 6e10 ≈ 8.33e-6`, so `m ≥ 1/ε ≈ 120,000` counters.

## Q zh
陈述 Space-Saving 算法（Metwally、Agrawal、El Abbadi 的定理 3）在流中寻找 Top-K 候选时的确定性保证，并计算：要保证捕获全天 600 亿事件窗口中所有观看量 ≥ 50 万的 item，需要多少个计数器 `m`？

## A zh
Space-Saving 只保留 `m` 个计数器：遇到一个未被监控的新元素时，淘汰当前值最小的计数器，把新元素的计数设为该最小值 + 1。定理 3 的保证不假设任何数据分布：只要 `m ≥ 1/ε`，任何真实频次 `f_i > ε*N` 的元素一定会出现在最终的监控集合里——这是零漏报保证，不是概率性的。要保证捕获所有全天观看量 ≥50 万的 item（N=6×10^10）：`ε = 500,000 / 6e10 ≈ 8.33e-6`，所以 `m ≥ 1/ε ≈ 120,000` 个计数器。
