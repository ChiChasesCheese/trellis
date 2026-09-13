---
id: dist-object-storage-key-layout
node: distributed.object-storage
type: qa
---
## Q
How should immutable page and image artifacts be keyed in object storage so deploy, cache, and rollback remain safe?

## A
Use a stable namespace plus tenant/project, immutable deployment or content digest, object kind, and canonical path/variant. Store media type, checksum, encoding, and generation metadata explicitly. Mutable aliases should be tiny conditional-updated pointers, not overwritten large objects. This makes retries idempotent, permits long cache TTLs, prevents cross-tenant collisions, and lets rollback select an existing snapshot without copying data.

## Q zh
immutable page/image artifact 在 object storage 中应如何设计 key，才能让 deploy、cache 和 rollback 安全？

## A zh
使用稳定 namespace，加 tenant/project、immutable deployment 或 content digest、object kind 与 canonical path/variant。显式存储 media type、checksum、encoding 和 generation metadata。mutable alias 应是通过 conditional update 修改的小型 pointer，而不是覆盖大型 object。这样 retry 可 idempotent、cache 可长 TTL、避免 cross-tenant collision，rollback 也能直接选择现有 snapshot 而无需复制数据。
