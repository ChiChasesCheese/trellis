---
id: polaris-why-catalog-needed
node: openplatform.polaris-catalog
type: qa
source: snowflake-docs
---
## Q
Iceberg 表的数据文件和元数据文件都已经在对象存储里了，为什么引擎还需要一个 catalog（目录服务）才能正确读写，而不能直接扫描存储目录？

## A
对象存储中的元数据文件本身并不标识哪个是最新快照，同一目录下可能同时存在新旧多个元数据文件，直接扫目录无法确定表的当前状态。catalog 保存“表名 → 当前元数据文件”的指针，并提供原子更新该指针的操作：读者据此找到唯一的当前快照，写者通过原子替换指针完成提交，多个引擎并发写入时也只有一个能成功推进指针。
