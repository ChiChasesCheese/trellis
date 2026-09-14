---
id: storage-json-contract-pitfalls
node: storage.encoding
type: qa
---
## Q
JSON is the default inter-service format anyway. Name its concrete weaknesses as a *data contract*, and what teams add to compensate.

## A
- **Numbers**: no int/float distinction, and integers beyond 2^53 silently lose precision in JS-lineage parsers — why Twitter-scale IDs ship as *strings*.
- **No binary type**: blobs go Base64 (+33% size).
- **No enforced schema**: compatibility lives in convention; nothing stops a producer renaming a field, and consumers find out at runtime.
- Verbose: field names repeated in every record (compression helps but parsing cost stays).

Compensations: **JSON Schema / OpenAPI** validation in CI, contract tests between producer and consumer, and switching to Protobuf/Avro with a registry where evolution guarantees must be machine-checked.

## Q zh
JSON 无论如何是默认的服务间格式。命名它作为**数据契约**的具体弱点，团队添加什么来补偿。

## A zh
- **数字**：无 int/float 区分，超过 2^53 的整数在 JS 系列解析器中无声丢失精度——为什么 Twitter 级别 ID 作为**字符串**发送。
- **无二进制类型**：blob 走 Base64（+33% 大小）。
- **无强制 schema**：兼容性存在于约定；没什么能阻止生产者重命名字段，消费者在运行时发现。
- 冗长：字段名在每条记录中重复（压缩有帮助但解析成本保持）。

补偿：CI 中的 **JSON Schema / OpenAPI** 验证，生产者和消费者之间的契约测试，切换到 Protobuf/Avro 配注册表，其中演进保证必须被机器检查。
