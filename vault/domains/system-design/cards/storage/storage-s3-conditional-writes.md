---
id: storage-s3-conditional-writes
node: storage.object
type: qa
---
## Q
S3's consistency model changed twice in the 2020s. What do you get now, and what new class of system did conditional writes unlock?

## A
- Since 2020: **strong read-after-write consistency** — a GET/LIST after any PUT (including overwrites) sees the latest version. The old eventual-consistency caveats are dead folklore.
- Since 2024: **conditional writes** — `If-None-Match: *` (create only if absent) and `If-Match: <etag>` (compare-and-swap on overwrite).

CAS on an object is a primitive for **coordination without a separate database**: multiple writers can safely race to commit — exactly what table formats need for atomic metadata-pointer swaps ([[analytics-lakehouse-snapshot-isolation]]), and it enables leases/locks and even S3-only queue/log designs. Losing writer gets `412 Precondition Failed` and retries against fresh state.

## Q zh
S3 的一致性模型在 2020 年代改变了两次。你现在得到什么，条件写解锁了什么新类系统？

## A zh
- 自 2020：**强读后写一致性**——任何 PUT 后的 GET/LIST（包括覆盖）看到最新版本。旧的最终一致性警告是死民俗。
- 自 2024：**条件写**——`If-None-Match: *`（仅当缺失时创建）和 `If-Match: <etag>`（覆盖时比较交换）。

对象上的 CAS 是**无需单独数据库的协调**的原始操作：多个写端可以安全竞争提交——正好是表格式为原子元数据指针交换需要的（[[analytics-lakehouse-snapshot-isolation]]），它启用租约/锁，甚至仅 S3 队列/日志设计。失败写端获得 `412 Precondition Failed` 并针对新鲜状态重试。
