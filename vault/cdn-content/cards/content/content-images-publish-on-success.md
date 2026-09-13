---
id: content-images-publish-on-success
node: content.images
type: qa
---
## Q
Two requests miss the same transformed image; one worker crashes mid-write. How should the pipeline avoid duplicate work and partial-cache hits?

## A
Collapse requests by the full derived-object key so one bounded transformation runs and peers wait or receive stale output. Write to a temporary object, verify decode/encode completion and checksum, then atomically publish or conditional-put the final key. A crash leaves only disposable temporary data. Cache negative deterministic failures briefly, but do not cache transient worker or dependency failures as permanent results.

## Q zh
两个请求同时 miss 同一张 transformed image，其中一个 worker 在写入中途 crash。pipeline 如何避免 duplicate work 和 partial-cache hit？

## A zh
按完整 derived-object key 合并请求，只运行一个有界 transformation，其他请求等待或接收 stale output。先写 temporary object，验证 decode/encode completion 与 checksum，再原子 publish 或 conditional-put final key。crash 只留下可丢弃的 temporary data。确定性 negative failure 可短暂缓存，但不要把 transient worker/dependency failure 缓存成永久结果。
