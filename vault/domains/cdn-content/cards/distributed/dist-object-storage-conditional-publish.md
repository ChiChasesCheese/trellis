---
id: dist-object-storage-conditional-publish
node: distributed.object-storage
type: qa
---
## Q
Two builders race to publish the same manifest key. How do conditional writes prevent lost updates?

## A
Read the current version/ETag, build the new immutable manifest, then update the live pointer with `If-Match` on the version observed—or use `If-None-Match: *` for create-once artifacts. One writer succeeds; the stale writer receives a precondition failure and must re-evaluate, not overwrite. Conditional writes turn a blind last-writer-wins race into explicit optimistic concurrency.

## Q zh
两个 builder 竞争 publish 同一个 manifest key。conditional write 如何避免 lost update？

## A zh
读取当前 version/ETag，构建新的 immutable manifest，再用针对已观察版本的 `If-Match` 更新 live pointer；create-once artifact 则用 `If-None-Match: *`。一个 writer 成功，stale writer 收到 precondition failure，必须重新评估而不是覆盖。conditional write 把盲目的 last-writer-wins race 转成显式 optimistic concurrency。
