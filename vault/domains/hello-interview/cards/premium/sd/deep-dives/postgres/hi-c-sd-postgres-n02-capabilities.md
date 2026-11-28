---
id: hi-c-sd-postgres-n02-capabilities
node: sd.deep-dives.postgres.notes
type: qa
step: 2
---
## Q
**PostgreSQL · 讨论 PostgreSQL 的四条主线**｜摘要 · 必会

面试里谈 PostgreSQL，应该围绕哪几个方面展开？有哪两种常见的失分方式？

## A
- **四条主线：** 读性能、写能力、一致性保证、复制。
- **失分方式一：** 一头扎进内部（MVCC、WAL）讲了半天，面试官只想知道它能不能撑住数据关系和规模。
- **失分方式二：** 说"NoSQL 比 PostgreSQL 扩展性好"这类笼统的话，没有分清场景和细节。
- **正确深度：** 先给出能力和限制，再用具体数字和做法说明什么时候够用、什么时候要分区或分片。
