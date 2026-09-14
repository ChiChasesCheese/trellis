---
id: storage-avro-evolution-defaults
node: storage.encoding
type: qa
---
## Q
In Avro, which schema changes keep *both* backward and forward compatibility, and why does the rule hinge entirely on default values? (Contrast with how Protobuf earns the same property.)

## A
The rule: you may **add or remove only a field that has a default value**.

Why defaults are the whole story — schema resolution matches writer's and reader's fields by name, and someone must fill the gap on each side:

- **Add field with default**: new reader ← old data: field absent, reader fills the default (backward ✓). Old reader ← new data: unknown field is skipped (forward ✓).
- **Remove field with default**: works mirrored — the side missing the field always has a default to fall back on.
- **Add a field *without* a default**: new readers crash on all old records — backward compatibility is gone (remove-without-default breaks forward, symmetrically).

Contrast: Protobuf gets the same guarantee structurally — all fields are optional with implicit defaults and unknown *tags* are skipped ([[storage-protobuf-tag-rules]]); Avro, having no tags, makes the default an explicit, per-field schema obligation that a schema registry can machine-check before accepting a new version.

## Q zh
在 Avro 里，哪些 schema 变更能*同时*保持 backward 和 forward 兼容，为什么这条规则完全取决于默认值？（对比 Protobuf 靠什么获得同样的性质。）

## A zh
规则：只允许**添加或删除带默认值的字段**。

为什么默认值是全部关键 — schema resolution 按名字匹配 writer 和 reader 的字段，两侧总得有人来填补缺口：

- **添加带默认值的字段**：新 reader ← 旧数据：字段缺失，reader 用默认值填上（backward ✓）。旧 reader ← 新数据：不认识的字段被跳过（forward ✓）。
- **删除带默认值的字段**：镜像地成立 — 缺字段的那一侧总有默认值可退。
- **添加*不带*默认值的字段**：新 reader 读所有旧记录都会失败 — backward 兼容没了（不带默认值的删除则对称地破坏 forward）。

对比：Protobuf 靠结构本身获得同样保证 — 所有字段都是 optional 且有隐式默认值、未知的 *tag* 被跳过（[[storage-protobuf-tag-rules]]）；Avro 没有 tag，于是把默认值变成每个字段显式的 schema 义务，schema registry 可以在接受新版本之前机器化校验它。
