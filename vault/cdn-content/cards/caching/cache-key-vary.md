---
id: cache-key-vary
node: caching.keys
type: qa
---
## Q
An origin selects WebP or JPEG from `Accept` but forgets `Vary: Accept`. What exact cache failure can occur?

## A
The first cached representation can be reused for clients whose `Accept` differs, so a client may receive an unsupported format. `Vary: Accept` tells a cache that the selecting request header participates in matching. Keep `Vary` consistent on `200` and `304`, and normalize to a small supported variant set to control cardinality.

## Q zh
origin 根据 `Accept` 选择 WebP 或 JPEG，却忘了 `Vary: Accept`。会发生什么具体 cache failure？

## A zh
第一个缓存的 representation 可能被复用于 `Accept` 不同的 client，导致 client 收到不支持的格式。`Vary: Accept` 告诉 cache：这个用于选择的 request header 必须参与 matching。`200` 与 `304` 的 `Vary` 要一致，并应归一化成少量受支持 variant，控制 cardinality。
