---
id: commit-write-then-swap-order
node: openplatform.external-engine-commit-protocol
type: cloze
source: snowflake-docs
---
一个外部引擎（如 Spark）向 Iceberg 表提交写入的顺序：先{{c1::把新的 Parquet 数据文件写入对象存储}}，再{{c2::写出引用这些文件的新清单（manifest）和新元数据文件}}，最后{{c3::在 catalog 中原子地把表的当前元数据指针从旧文件替换为新文件}}。只有最后一步成功，这次写入才对读者可见。
