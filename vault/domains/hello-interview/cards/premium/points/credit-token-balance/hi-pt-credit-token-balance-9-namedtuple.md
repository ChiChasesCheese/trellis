---
id: hi-pt-credit-token-balance-9-namedtuple
node: qb.lld.credit-token-balance.points
type: qa
step: 9
---
## Q
**额度账本 · NamedTuple 返回值**｜追问 · 出自：额度账本 › 取舍与追问

`charge` 返回的分配列表里每一项是（包 id，金额）。用普通元组、数据类还是别的？

## A
**选择。** `NamedTuple`：`Allocation(grant_id, amount)`。

**为什么。** 既能像元组一样比较、拆包（`for gid, amount in allocations`），又有字段名；普通元组让调用方记位置，数据类又要多写比较。
