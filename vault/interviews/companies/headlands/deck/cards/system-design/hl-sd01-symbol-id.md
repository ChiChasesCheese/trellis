---
id: hl-sd01-symbol-id
node: system-design.sd01-unused-code
type: qa
step: 14
---
## Q
索引记录的三张表是什么？符号 ID 怎么生成，碰撞概率多大？

## A
- `defs`：(sym_id int64, kind {CLASS, METHOD, FIELD, TARGET, RESOURCE}, fqn, desc, access, file, line, owner)；
- `refs`：(src_id, dst_id, kind {CALL, NEW, EXTENDS, IMPLEMENTS, FIELD_R, FIELD_W, ANNOT, METHOD_REF})；
- `strs`：(file_or_class, literal)。

`sym_id` = **64 位哈希**（FQN + 描述符 + 种类），所以不同分片独立计算也得到同一个 ID，汇总时只需按 ID 排序 / 分组。碰撞概率：n = 3.2×10⁶ 个符号，生日界约 n²/2⁶⁵ = (3.2×10⁶)² / 3.7×10¹⁹ ≈ **2.8×10⁻⁷**，可忽略；汇总时再校验同 ID 下 FQN 一致，碰撞则报警。记录追加式、不可变，分片失败只重跑该分片。
