---
id: cc-chrono-arithmetic-month-end-clamp
node: chrono.arithmetic
type: cloze
---
A subscription anchored on the {{c1::31}}st and billed monthly must clamp to the shortest month: one month after 2025-01-31 is {{c2::2025-02-28}}, and one month after *that* must return to {{c3::2025-03-31}}. So the anchor day is stored once and clamped per period — overwriting the anchor with the clamped value makes it {{c4::stick at 28}} forever. In a leap year the same anchor clamps to {{c5::2024-02-29}} instead.

## zh
以每月 {{c1::31}} 号为锚点的订阅必须向最短的月份钳位：2025-01-31 之后一个月是 {{c2::2025-02-28}}，*再*一个月必须回到 {{c3::2025-03-31}}。所以锚点日只存一次、每期单独钳位 —— 用钳位后的值覆盖锚点会让它永远 {{c4::卡在 28}}。闰年里同一个锚点则钳位到 {{c5::2024-02-29}}。
