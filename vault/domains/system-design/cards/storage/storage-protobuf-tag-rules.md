---
id: storage-protobuf-tag-rules
node: storage.encoding
type: qa
---
## Q
In Protobuf, what identifies a field on the wire, and what are the evolution rules that follow from it?

## A
The **field tag number** — the wire format carries `(tag, wire-type, value)`, never field names. Hence:

- **Renaming a field is free** (names are code-only); **changing its tag breaks everything** — old data decodes into the wrong field.
- **Never reuse a removed field's tag** (`reserved` it): old records with that tag would silently decode as the new field. Silent corruption, not an error.
- **New fields must be optional / have defaults** so old data (which lacks them) still parses — backward compat.
- Old code skips **unknown tags** using the wire type to know how many bytes to skip — forward compat.

## Q zh
在 Protobuf 中，什么标识线上的字段，随之而来的演进规则是什么？

## A zh
**字段标签号**——线格式携带 `(tag, wire-type, value)`，永远不是字段名。因此：

- **重命名字段是免费的**（名称只在代码中）；**改变它的标签破裂一切**——旧数据解码到错误的字段。
- **永远不要重用被移除字段的标签**（`reserved` 它）：带那个标签的旧记录会无声地解码为新字段。无声损坏，不是错误。
- **新字段必须是可选的/有默认值**所以旧数据（缺乏它们）仍然解析——向后兼容。
- 旧代码**跳过未知标签**使用线类型知道跳过多少字节——前向兼容。
