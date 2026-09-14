---
id: compression-columns-stored-independently
node: storage.columnar-compression-encoding
type: qa
source: snowflake-docs
---
## Q
为什么在微分区（micro-partition）内“每列独立存储、独立压缩”是查询只读取所需列的前提？

## A
列式存储（columnar storage）把同一列的数据放在一起并单独压缩，每列都是可以单独定位、单独解压的一段数据。于是查询只需读取并解压它引用的那几列，其他列的数据完全不碰；如果按行存储，各列的值交错在一起，读一列就必须把整行一起读出和解压。
