---
id: hi-pt-tt-double-entry-ledger-3-post
node: tt.lld.tt-double-entry-ledger.points
type: qa
step: 3
---
## Q
**复式账本（类设计） · post 的幂等与平衡检查**｜出自：复式账本（类设计） › 整体设计

`post(entry)` 的处理顺序是什么？重复提交和内容不同的复用 ID 怎么处理？

## A
**顺序。** 先查 `_by_id`：重复就返回原序号，ID 相同但内容不同则报错；否则按币种汇总各腿，要求腿数 ≥ 2 且每个币种合计为 0；通过后在同一个临界区内追加日志、登记去重表、更新每个账户余额并追加历史。
**数据库。** `(分录 ID)` 唯一约束就是去重。
