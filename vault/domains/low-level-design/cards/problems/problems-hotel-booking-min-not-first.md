---
id: problems-hotel-booking-min-not-first
node: problems.booking.hotel-booking
type: qa
step: 3
tags: [grown]
---
## Q
酒店预订中"这段日期还能订几间"应该取区间里第一晚的剩余量、平均值，还是最小值？为什么？

## A
取**最小值**。一段连住只要有一晚满了，整段就订不了——客人不可能住一半换家酒店，所以可订量由最紧的那一晚决定，首晚宽松完全不能代表整段。代码就是 `min(available_on(t, n) for n in stay.each_night())`。取首晚是最常见的错法，它会让搜索结果里出现一堆点进去才发现订不了的酒店；取平均更糟，它会把一个 0 稀释掉，直接导致超卖。这条规则同时解释了为什么搜索只是"建议"、真正的裁决必须发生在下单时那一次原子的检查加写入里。
