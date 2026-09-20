---
id: problems-auction-soft-close-expected-extension-needs-cap
node: problems.commerce.auction
type: qa
step: 5
tags: [grown]
---
## Q
A soft-close rule resets a 60-second countdown to 60 seconds every time a new bid arrives within that window. Modeling a hot auction's late-stage bid arrivals as Poisson with an average of one bid every 20 seconds (lambda = 0.05/sec), the probability of a 60-second gap with no bid is e^(-0.05*60) = e^(-3) ≈ 0.0498, so the expected number of 60-second windows before the auction naturally closes is about 1/0.0498 ≈ 20.1, for an expected total extension of about 20.1 x 60 ≈ 1,205 seconds (~20 minutes). What design implication follows from this number?

## A
A pure soft-close rule with no other bound has no guaranteed end time — under sustained bidding, expected extension is unbounded in principle and, even under this modest arrival rate, already averages about 20 minutes past the original close time. This means soft-close must be paired with a hard ceiling on total extension time (or a rule that tightens the window after repeated extensions), otherwise a sufficiently persistent bidder (or coordinated bidding) could keep an auction open indefinitely, which is an unacceptable product outcome even though it isn't a correctness bug.

## Q zh
一条软关闭（soft close）规则规定：只要在最后 60 秒的窗口内出现新出价，倒计时就重置为 60 秒。把一场热门拍卖后期的出价到达建模为泊松过程，平均每 20 秒一次（λ = 0.05/秒），则 60 秒窗口内没有出价的概率是 e^(-0.05×60) = e^(-3) ≈ 0.0498，因此拍卖自然结束前预期要经历约 1/0.0498 ≈ 20.1 个 60 秒窗口，预期总延长时间约为 20.1 × 60 ≈ 1,205 秒（约 20 分钟）。这个数字带来了什么设计上的含义？

## A zh
单纯的软关闭规则如果不加其他约束，就没有确定的结束时间上限——在持续出价的情况下，理论上预期延长时间是无界的，即使在这个并不算激进的到达速率假设下，平均也已经比原定结束时间多拖了约 20 分钟。这意味着软关闭必须搭配一个总延长时间的硬上限（或者在多次延长后收紧窗口的规则），否则足够持久的出价者（或者协同刷单）理论上可以让拍卖无限期不结束——这虽然不是正确性 bug，但在产品层面是不可接受的结果。
