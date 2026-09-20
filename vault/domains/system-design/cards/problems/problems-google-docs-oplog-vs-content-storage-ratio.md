---
id: problems-google-docs-oplog-vs-content-storage-ratio
node: problems.media.google-docs
type: qa
step: 1
tags: [grown]
---
## Q
In a collaborative document editor, why does storing every raw edit operation forever (for full undo/version history) cost roughly an order of magnitude more storage per year than the documents' actual content, and what design change does that force?

## A
Every keystroke-level operation (type, position, content delta, author, timestamp) is a small durable record, and an actively-edited platform produces far more operation records per year than new document bytes, because most edited characters are typed, revised, and deleted many times before a document settles — one worked estimate puts raw operation-log growth at roughly 11.5x the new document content storage. This forces a two-tier retention design: keep fine-grained operations only for a rolling recent window (supporting precise undo/history browsing), and compact everything older into periodic named snapshots, discarding the intermediate operations rather than keeping them forever.

## Q zh
在协同文档编辑器中，为什么无限期保留每一次原始编辑操作（为了支持完整的撤销/版本历史）每年的存储成本会比文档实际内容本身高出一个数量级左右，这个事实迫使设计做出什么改变？

## A zh
每一条按键级操作记录（类型、位置、内容增量、作者、时间戳）都是一条小的持久化记录，而一个被持续编辑的平台每年产生的操作记录量远超新增文档字节量，因为大多数被编辑的字符在文档定稿前会被反复输入、修改、删除——一个估算给出原始操作日志的增长量级约为新增文档内容存储量的 11.5 倍。这迫使设计采用两层保留策略：只在一个滚动的近期窗口内保留细粒度操作（支持精确的撤销/历史浏览），窗口之外的全部压缩成周期性的命名快照，丢弃中间的细粒度操作而不是永久保留。
