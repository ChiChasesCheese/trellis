---
id: parameter-category-order-cloze
node: functions.arguments
type: cloze
source: python-docs
---
一个函数的参数列表从左到右，类别固定按 {{c1::仅位置参数（positional-only，写在 `/` 之前）}} → 位置或关键字参数 → {{c2::仅关键字参数（keyword-only，写在 `*` 或 `*args` 之后）}} 排列，收尾多余参数的 `**kwargs` 必须放在整个参数列表的{{c3::最后一位}}。
