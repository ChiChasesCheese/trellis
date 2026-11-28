---
id: hi-pt-restaurant-waitlist-api-12-change-size
node: qb.lld.restaurant-waitlist-api.points
type: qa
step: 12
---
## Q
**餐厅候位 API · 改人数**｜加分 · 出自：餐厅候位 API › 逐步扩展 4

排队的客人想把 4 人改成 2 人。`change_size` 要保证什么，改小后会发生什么？

## A
**要点。** 先校验（不在排队抛 `UnknownPartyError`，新人数不合法同 `join`），失败队伍原样；再改人数，位置和被插队次数不变，最后调统一收尾 `_seat_everyone_possible()`。

**结果。** 改小后可能立刻坐下，也可能带动后面被挡住的人，返回因此新入座的 `(party_id, 桌号)`。
