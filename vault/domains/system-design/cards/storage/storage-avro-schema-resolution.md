---
id: storage-avro-schema-resolution
node: storage.encoding
type: qa
---
## Q
Avro encodes no field names *and* no tag numbers — just values in order. How can a reader with a different schema version decode it?

## A
Decoding requires the exact **writer's schema**; the reader then performs **schema resolution** against its own **reader's schema**: fields matched **by name** (order may differ), reader-only fields filled from defaults, writer-only fields skipped.

Where the writer's schema comes from without bloating every record:
- **Files**: schema once in the file header, millions of records after it.
- **Kafka**: a **schema registry** — each message carries a small schema ID.

Payoff vs Protobuf: no tag-number bookkeeping, so schemas can be **generated dynamically** (e.g. from a DB schema per table) — which is why Avro dominates data-pipeline/CDC tooling.

## Q zh
Avro 既不编码字段名也不编码标签号——只编码值的顺序。读端如何用不同的 schema 版本解码？

## A zh
解码需要准确的 **writer's schema**；读端随后用自己的 **reader's schema** 执行 **schema resolution**：字段按**名字**匹配（顺序可能不同），只读字段从默认值填充，只写字段被跳过。

writer's schema 从哪里来而不膨胀每条记录：
- **Files**：schema 一次在文件头，数百万条记录之后。
- **Kafka**：一个 **schema registry**——每条消息携带一个小的 schema ID。

相比 Protobuf 的好处：无需标签号记账，所以 schema 可以被**动态生成**（例如每个表的 DB schema）——这就是为什么 Avro 在 data-pipeline/CDC 工具中占主导。
