---
id: copy-into-parallel-across-files
node: ingestion.bulk-copy-into
type: qa
source: snowflake-docs
---
## Q
要从暂存区（stage）批量加载 1 TB 数据，为什么通常建议拆成大量中等大小的文件，而不是一个巨大的单文件？仓库规格又该怎么选？

## A
COPY 以文件为单位把加载工作分配到仓库的多个计算资源上并行执行，文件越多、大小越均匀，并行度越高；一个巨大的单文件难以被充分并行处理。仓库规格应与要加载的文件数量和每个文件的数据量相匹配：文件多、数据量大时用更大的仓库提升并行度，由于按秒计费，加载完即可挂起。
