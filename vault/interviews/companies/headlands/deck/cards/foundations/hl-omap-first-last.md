---
id: hl-omap-first-last
node: foundations.ordered-maps-trees
type: qa
step: 22
---
## Q
`firstKey()` 与 `firstEntry()`、`pollFirstEntry()` 在空 Map 上分别怎么表现？为什么循环里应该用 `firstEntry()` 并判 `null`？

## A
- `firstKey()` / `lastKey()`：返回最小 / 最大 key，空 Map 上**抛** `NoSuchElementException`；
- `firstEntry()` / `lastEntry()`：返回最小 / 最大条目（如 `101=50`），空 Map 返回 `null`；
- `pollFirstEntry()` / `pollLastEntry()`：取出并删除最小 / 最大，空返回 `null`。

循环里用 `firstEntry()` 并判 `null`（或先 `isEmpty()`），不要靠 `firstKey()` 抛异常来判空。
