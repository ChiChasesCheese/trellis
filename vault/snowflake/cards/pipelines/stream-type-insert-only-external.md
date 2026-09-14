---
id: stream-type-insert-only-external
node: pipelines.stream-types
type: qa
source: snowflake-docs
---
## Q
外部表（external table）上能建哪种流？云存储中一个文件被覆盖重写后，这种流会返回什么？

## A
外部表、外部管理的 Iceberg 表和不带分区列的 Delta Direct 表只支持仅插入流（insert-only stream）。它只追踪行插入，不记录删除。覆盖或追加过的文件被视为新文件：旧版本从云存储移除，但流不记录这次删除；新版本的所有行都作为插入返回，流不会计算新旧文件的差异。因为云存储中文件的历史版本不受 Snowflake 管理，也无法保证可访问。
