---
id: stream-row-change-metadata-columns
node: pipelines.stream-offset-bookmark
type: cloze
source: snowflake-docs
---
查询流时，除了与源对象相同的列之外，还会返回三个元数据列：{{c1::`METADATA$ACTION`}}（记录的 DML 操作：INSERT 或 DELETE）、{{c2::`METADATA$ISUPDATE`}}（该操作是否属于 UPDATE；UPDATE 表现为一对 DELETE+INSERT 记录，此列为 TRUE）、{{c3::`METADATA$ROW_ID`}}（用于跨时间追踪变更的唯一且不可变的行 ID）。
