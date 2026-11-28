---
id: hi-pt-restaurant-waitlist-api-11-replace-copy
node: qb.lld.restaurant-waitlist-api.points
type: qa
step: 11
---
## Q
**餐厅候位 API · 副本推演与 replace**｜追问 · 出自：餐厅候位 API › 深入 4

估计要在队伍副本上推演，副本必须带上每个人的被插队次数。复制队伍时用什么写法，加了新字段还安全吗？

## A
**写法。** `dataclasses.replace(w)` 复制所有字段：`[replace(w) for w in self._queue]`。后来给 `_Waiting` 加 `skipped` 字段，复制代码不用改。

**易错。** 手写 `_Waiting(w.id, w.size)` 会漏掉新字段，估计与真实行为脱节。

**配合。** `_Waiting` 是 `@dataclass(slots=True)`，可变但只在模块内部使用（内部可变、外部只读）。
