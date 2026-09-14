---
id: cc-toolbox-cache-ttl
node: toolbox.cache
type: cloze
---
An entry written at `time` with a `ttl` is alive on the half-open range {{c1::`[time, time + ttl)`}} — readable at `time + ttl - 1`, expired at `time + ttl` — so `ttl = 0` means {{c2::never readable at all}}. Expire **lazily** at read (`if now >= expiry: miss`) rather than sweeping every key on every tick; a background sweep exists only to {{c3::reclaim memory}} and must never change {{c4::what a read returns}}.

## zh
在 `time` 写入、带 `ttl` 的条目存活于半开区间 {{c1::`[time, time + ttl)`}} —— 在 `time + ttl - 1` 可读，在 `time + ttl` 已过期 —— 所以 `ttl = 0` 意味着 {{c2::根本永远不可读}}。在读取时**惰性**过期（`if now >= expiry: miss`），而不是每个时钟节拍扫描所有 key；后台清扫只是为了 {{c3::回收内存}}，绝不能改变 {{c4::读取返回的结果}}。
