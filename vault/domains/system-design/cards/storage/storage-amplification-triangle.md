---
id: storage-amplification-triangle
node: storage.internals.tradeoffs
type: cloze
---
Storage engines juggle three amplifications you can't minimize simultaneously: {{c1::write amplification}} (bytes physically written per byte of user write — LSM compaction rewrites data many times), {{c2::read amplification}} (structures consulted per lookup — LSM reads may touch many SSTables, B-trees ~one path), and {{c3::space amplification}} (disk used vs live data — LSM holds obsolete versions until compaction; B-trees carry fragmented half-empty pages). Leveled compaction trades higher write amp for lower read/space amp; size-tiered does the reverse.

## zh
存储引擎需要在三种放大效应之间权衡（无法同时最小化所有三种）：{{c1::write amplification}}（每字节用户写对应的物理写字节数——LSM 压实会重写数据多次），{{c2::read amplification}}（查询需要访问的结构——LSM 读可能触及多个 SSTable，B 树约一条路径），和 {{c3::space amplification}}（磁盘使用量与活跃数据比——LSM 在压实前保存过期版本；B 树有碎片化的半满页）。Leveled 压实用更高的 write amp 换取更低的 read/space amp；size-tiered 则反过来。
