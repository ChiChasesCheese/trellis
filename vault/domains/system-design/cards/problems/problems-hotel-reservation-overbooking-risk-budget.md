---
id: problems-hotel-reservation-overbooking-risk-budget
node: problems.commerce.hotel-reservation
type: qa
step: 5
tags: [grown]
---
## Q
Using a binomial no-show model with a historical no-show rate of 6%, why is a flat 'overbook by 2%' policy unsafe for a 50-room inventory pool but overly conservative for a 500-room pool, if the target risk of actually exceeding physical capacity is 1%?

## A
For a 50-room pool, overbooking to 51 bookings (+2%) already gives about a 4.26% chance that actual arrivals exceed 50 rooms (no-shows among 51 bookings, modeled as Binomial(51, 0.06), need to number fewer than 1) — over 4x the 1% risk budget, so a small pool has almost no safe overbooking headroom at that risk tolerance. For a 500-room pool, the same 6% no-show rate allows overbooking all the way to 519 bookings (+3.8%) while staying within the 1% risk budget, because the binomial distribution's relative variance shrinks as the pool grows (law of large numbers). A correct overbooking policy therefore computes its safe percentage from pool size and historical no-show rate per room-type, rather than applying one constant percentage everywhere.

## Q zh
用一个历史不入住率（no-show rate）为 6% 的二项分布模型，如果可接受的超容风险目标是 1%，为什么统一的「超售 2%」策略对一个 50 间房的库存池不安全，对一个 500 间房的库存池又过于保守？

## A zh
对 50 间房的池子，超售到 51 笔预订（+2%）时，实际到店人数超过 50 间的概率就已经约有 4.26%（51 笔预订中不入住数服从 Binomial(51, 0.06)，需要少于 1 次才安全）——已经超过 1% 风险预算的 4 倍以上，说明小库存池在这个风险容忍度下几乎没有安全的超售空间。对 500 间房的池子，同样 6% 的不入住率可以超售到 519 笔预订（+3.8%）仍能控制在 1% 风险预算内，因为二项分布的相对方差随池子规模增大而收窄（大数定律）。所以正确的超售策略应该按每个房型的库存池规模和历史不入住率动态计算安全比例，而不是到处套用同一个固定百分比。
