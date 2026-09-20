---
id: problems-object-storage-wide-ec-more-durable-than-triple-replication
node: problems.foundations.object-storage
type: qa
step: 4
tags: [grown]
---
## Q
Using a simplified failure model of independent per-drive annual failures at a 1.36% rate (a real observed annualized failure rate), a triple-replication stripe (3 fragments, tolerates 2 simultaneous failures, object lost only if all 3 fail) has an annual per-stripe loss probability of about 2.52x10^-6, while a Reed-Solomon(10,4) erasure-coded stripe (14 fragments, tolerates 4 simultaneous failures) has about 8.41x10^-7 - roughly 3x lower - despite RS(10,4) using only 1.4x storage versus triple replication's 3x. Why does the wider scheme end up more durable with less storage, rather than less durable?

## A
Durability under this binomial model isn't driven by the raw storage multiplier, it's driven by how many simultaneous fragment failures a stripe can absorb before data is lost - the 'tolerance count' - relative to how quickly the probability of exceeding that count grows with more independent chances to fail. Triple replication tolerates only 2 simultaneous failures out of 3 fragments; RS(10,4) tolerates 4 simultaneous failures out of 14. Even though RS(10,4) has more fragments that could individually fail, the binomial tail probability of exceeding a tolerance of 4 drops off faster than the tail probability of exceeding a tolerance of 2, so the absolute tolerance count matters more than the fragment count or the storage ratio - a wider stripe with a proportionally higher absolute parity count can be both cheaper and more durable than a narrow, high-multiplier replication scheme.

## Q zh
用一个简化的失效模型（各盘独立，年故障率 1.36%，这是一个真实观测到的年化故障率），三副本条带（3 个分片，容忍 2 个同时失效，只有 3 个都坏才算丢）年丢失概率约为 2.52×10⁻⁶，而 Reed-Solomon(10,4) 纠删码条带（14 个分片，容忍 4 个同时失效）约为 8.41×10⁻⁷，低约 3 倍——尽管 RS(10,4) 只用 1.4 倍存储而三副本用 3 倍。为什么更宽的方案反而用更少存储得到更高的耐久性，而不是更低？

## A zh
在这个二项分布模型下，耐久性不由原始存储倍数决定，而由「一个条带在数据丢失前能吸收多少个同时失效」——即容忍数——相对于「超过这个容忍数的概率随独立失败机会增多而增长的速度」决定。三副本在 3 个分片中只容忍 2 个同时失效；RS(10,4) 在 14 个分片中容忍 4 个同时失效。即使 RS(10,4) 有更多分片可能单独失效，超过「容忍 4」这个阈值的二项分布尾部概率下降得比超过「容忍 2」更快，所以绝对容忍数比分片数或存储比例更关键——一个更宽、校验比例相对更高的条带，可以同时比窄窄的高倍数副本方案更便宜、更耐久。
