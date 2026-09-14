---
id: pruning-zonemap-mechanism
node: pruning.min-max-zone-maps
type: qa
source: snowflake-docs
---
## Q
Snowflake 要跳过一个微分区（micro-partition）而不去打开它读取数据，靠的是什么信息，判断发生在什么阶段？

## A
每个微分区的头部元数据里记录了该分区中每一列的最小值/最大值范围（即 zone map）。查询编译时，优化器把查询谓词（predicate）的取值范围与每个微分区各列的最小/最大值范围比较：如果谓词要求的范围与该分区的范围完全不相交，就整块跳过这个微分区，连打开文件扫描都不需要。这个判断发生在编译期（而不是执行期逐行过滤），所以代价很低。
