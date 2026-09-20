---
nodes: [problems.machines.parking-lot]
url: https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/parking-lot
tags: [no-archive]
---
# Hello Interview — Parking Lot

值得读：把机考的推进节奏讲得很清楚——先澄清范围（几种车型、要不要收费、要不要多层），
再给核心实体（`ParkingLot`/`ParkingSpot`/`Ticket`），最后单独一节讲"追问会往哪三个方向
走"（多楼层、按车型差异化计费、多入口并发），本文"45 分钟怎么分配"和"扩展与追问"两节
参考了这个节奏。它建议的计价是"全场统一按小时收费"，比本文实现的单一策略更简单；本文
额外做了按车型和阶梯计价，是因为"计费策略可换"本来就是这道题被考察的点之一，不能简化掉。
