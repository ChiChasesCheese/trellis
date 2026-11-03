---
id: hi-sd-dropbox-5-sharing
node: sd.problem-breakdowns.dropbox.exam
type: qa
step: 5
---
## Q
**Dropbox：分享关系的存法**｜系统设计 · 问题拆解

Dropbox 里怎样存储「文件分享给了谁」，才能让用户快速列出别人分享给自己的文件？比较在元数据里放 sharelist、再加反向缓存、单独建分享表三种做法。

## A
**差：元数据里放 sharelist。** 查「我的文件」可用 uploadedBy 索引，但查「分享给我的文件」要扫描每个文件的 sharelist，很慢。

**中：加反向缓存。** 在 sharelist 之外再维护 `用户 -> 文件列表` 的映射，打开页面直接查。代价是两份数据要保持同步，最好放在同一个数据库里用事务同时更新。

**好：单独的 SharedFiles 表（范式化）。** 以 userId 为分区键、fileId 为排序键组成复合主键，每行表示一次分享。查某用户被分享的文件就是按分区键查询；元数据里不再放 sharelist，也就没有同步问题。

**取舍。** 走索引查询比纯键值查找略慢，但换来不需要维护两份数据，通常值得。这张表也是下载时校验权限的依据。
