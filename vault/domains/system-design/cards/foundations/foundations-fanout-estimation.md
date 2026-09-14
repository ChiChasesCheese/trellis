---
id: foundations-fanout-estimation
node: foundations.estimation
type: qa
---
## Q
Twitter-style home timelines: ~5k tweets/s written, ~300k timeline reads/s, avg 75 followers. Walk the fan-out-on-write math and the estimate that breaks it.

## A
Fan-out on write: 5k tweets/s × 75 followers ≈ **375k timeline-cache inserts/s** — heavy but feasible, and it makes the dominant operation (reads) a cheap precomputed lookup.

The **tail of the distribution** breaks it: one 100M-follower account tweeting = 100M inserts for a single event — impossible within a delivery SLO. Hence the hybrid: push for normal users, pull celebrity tweets at read time and merge.

Lesson: estimate with the skew, not the mean — averages hide the case that forces the design.


## Q zh
Twitter 风格的主页推送流：~5k tweets/s 写入、~300k 推送流读取/s、平均 75 个关注者。走通 fan-out-on-write 的数学和突破它的估算。

## A zh
写入时 fan-out：5k tweets/s × 75 个关注者 ≈ **375k 推送流缓存插入/s** — 繁重但可行，且它让主流操作（读取）成为便宜的预计算查找。

**分布的尾部**突破它：一个 1 亿粉丝的账户发推 = 单个事件 1 亿次插入 — 无法在交付 SLO 内完成。因此采用混合方案：对普通用户推送，在读取时拉取名人推文并合并。

教训：用偏差而不是平均值估算 — 平均值隐藏了强制设计改变的情况。
