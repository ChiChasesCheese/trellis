---
id: spill-memory-local-remote-order
node: query.spilling-to-remote-disk
type: cloze
source: snowflake-docs
---
当某个算子（例如对海量数据做去重）的中间结果超出执行服务器的可用内存时，Snowflake 查询引擎先把数据溢出（spilling）到 {{c1::本地磁盘（local disk）}}；本地磁盘空间也不够时，再溢出到 {{c2::远程磁盘（remote disk）}}。其中溢出到 {{c3::远程磁盘}} 对查询性能的影响最为严重。
