---
id: hl-j09-ex-linkedhashmap
node: java21.j09-sequenced-collections
type: qa
step: 22
---
## Q
`LinkedHashMap` 初始 `{x=1, y=2, z=3}`：`put("x", 10)`、`putLast("x", 11)`、`putFirst("w", 0)`、`pollFirstEntry()` + `pollLastEntry()` 依次得到什么？

## A
- `put("x", 10)` → `{x=10, y=2, z=3}`（已存在 key：只改值，位置不变）；
- `putLast("x", 11)` → `{y=2, z=3, x=11}`（改值并挪到最后）；
- `putFirst("w", 0)` → `{w=0, y=2, z=3, x=11}`（新 key 加到最前）；
- `pollFirstEntry()` 得 `w=0`，`pollLastEntry()` 得 `x=11`，剩 `{y=2, z=3}`。

另外 `sequencedKeySet().getLast()` 取最后一个 key，`sequencedValues().getFirst()` 取第一个 value。
