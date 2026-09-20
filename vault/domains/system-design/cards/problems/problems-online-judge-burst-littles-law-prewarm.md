---
id: problems-online-judge-burst-littles-law-prewarm
node: problems.realtime.online-judge
type: qa
step: 1
tags: [grown]
---
## Q
In an online judge design for a contest with 80,000 arriving contestants, if 50% of them submit at least once within the first 5 minutes (a burst rate of about 133 submissions/second) and each submission occupies a sandbox for an average of 4 seconds end-to-end, how many concurrent sandboxes does Little's Law say the system needs at the burst, and why does this favor pre-warmed capacity over reactive autoscaling?

## A
Little's Law gives concurrency = arrival rate x service time = 133.3 x 4 ≈ 533 concurrent sandboxes needed at the burst, versus roughly 32 in steady state — about a 17x jump. A reactive autoscaler that scales on CPU or queue depth typically takes several minutes to detect load and boot new capacity, slower than the burst itself, which arrives within about a minute of contest start. Because the contest start time and registrant count are both known in advance, the system instead pre-warms worker capacity to the computed concurrency a few minutes before the bell, with reactive autoscaling only absorbing overflow beyond that.

## Q zh
在一个在线判题系统设计中，一场竞赛有 8 万名到场参赛者，如果其中 50% 会在开考后前 5 分钟内至少提交一次（爆发速率约每秒 133 次提交），且每次提交平均占用沙箱 4 秒，利特尔法则（Little's Law）算出爆发期需要多少并发沙箱？为什么这个结果更支持预热式容量而不是被动式自动伸缩？

## A zh
利特尔法则给出并发度 = 到达速率 × 服务时间 = 133.3 × 4 ≈ 533 个并发沙箱，而常态下大约只需要 32 个——跳变约 17 倍。基于 CPU 或队列深度触发的被动式自动伸缩通常需要几分钟才能检测到负载并拉起新容量，比开考约一分钟内就到来的爆发本身还慢。由于开考时间和报名人数都是提前已知的，系统改为在开考前几分钟把工作节点容量预热到算出的这个并发度，被动式伸缩只用来吸收预热容量之外的额外波动。
