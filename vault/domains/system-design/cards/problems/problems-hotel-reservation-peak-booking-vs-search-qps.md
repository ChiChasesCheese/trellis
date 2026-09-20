---
id: problems-hotel-reservation-peak-booking-vs-search-qps
node: problems.commerce.hotel-reservation
type: qa
step: 1
tags: [grown]
---
## Q
A hotel/marketplace reservation platform processes 1,000,000 bookings/day and, at a 2% search-to-booking conversion rate, 50,000,000 search sessions/day. What is the average read:write QPS ratio, and why can this system get away with a much smaller booking peak-to-average ratio than a single-event ticket sale?

## A
Average booking QPS ≈ 1,000,000 / 86,400 ≈ 11.6; average search QPS ≈ 50,000,000 / 86,400 ≈ 578.7; the read:write ratio is about 50:1. Unlike a ticket sale, where demand concentrates on one scarce resource at one instant (peak-to-average ratios in the hundreds), hotel/marketplace demand is spread across millions of independently-booked room-types, so a modest peak-to-average factor (e.g. 5x, giving roughly 58 peak booking QPS) is enough — booking traffic never needs a virtual admission queue to survive its peak; only the 50:1 read:write gap forces search onto a separate read path from booking.

## Q zh
一个酒店/民宿预订平台每天处理 100 万笔预订，按 2% 的搜索到预订转化率计算，每天有 5000 万次搜索会话。平均读写 QPS 比是多少？为什么这个系统能接受比单场演出票务开售小得多的预订峰谷比？

## A zh
平均预订 QPS ≈ 1,000,000 / 86,400 ≈ 11.6；平均搜索 QPS ≈ 50,000,000 / 86,400 ≈ 578.7；读写比约为 50:1。和票务开售不同（需求在同一瞬间集中在同一批稀缺资源上，峰谷比可达数百倍），酒店/民宿的需求分散在数百万个独立可预订的房型上，所以一个不算大的峰谷因子（比如 5 倍，对应峰值预订 QPS 约 58）就够用——预订路径不需要虚拟准入队列来扛峰值，真正逼出架构决策的是 50:1 这个读写比，它要求搜索走一条独立于预订的读路径。
