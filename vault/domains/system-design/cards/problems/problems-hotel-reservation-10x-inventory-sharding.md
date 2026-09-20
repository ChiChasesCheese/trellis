---
id: problems-hotel-reservation-10x-inventory-sharding
node: problems.commerce.hotel-reservation
type: qa
step: 8
tags: [grown]
---
## Q
In a hotel/marketplace reservation system storing one inventory row per room-type per night over a 365-day booking window, what happens to the inventory table's row count at 10x listing scale (6 million to 60 million listings), and what architectural change does that force?

## A
Row count scales linearly with listings: at 6 million listings (about 9 million room-types) the table holds roughly 3.3 billion rows; at 60 million listings it grows to roughly 33 billion rows, which starts to strain even a sharded relational cluster. This forces the inventory table toward coarser geographic physical sharding (on top of sharding by room-type) and time-window tiering — keeping the near-term booking window (e.g. the next 90 days, where the overwhelming majority of bookings land) on high-performance storage while pushing the far-future window to cheaper storage, rather than treating the full 365-day window as uniformly hot.

## Q zh
在一个按'每个房型每晚一行、开放未来 365 天预订窗口'存储库存的酒店/民宿预订系统里，房源数增长 10 倍（600 万到 6000 万）时，库存表的行数会发生什么变化？这会迫使架构做出什么改变？

## A zh
行数随房源数线性增长：600 万房源（约 900 万房型）时库存表约有 32.85 亿行；6000 万房源时会涨到约 328.5 亿行，此时即便是分片良好的关系型集群也开始吃力。这会迫使库存表转向更粗粒度的地理物理分片（在按房型分片之上再加一层），并按时间窗口做分层存储——把近期预订窗口（比如未来 90 天，绝大多数预订都落在这个区间）放在高性能存储上，把更远的窗口挪到更廉价的存储上，而不是把整个 365 天窗口都当成同等热度的数据对待。
