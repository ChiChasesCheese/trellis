---
id: stream-type-choice-cloze
node: pipelines.stream-types
type: cloze
source: snowflake-docs
---
按源对象选择流类型：标准表、动态表、视图上需要完整的 INSERT/UPDATE/DELETE 净变化，用{{c1::标准流（standard）}}；同样的对象只关心新增行（如 ELT 暂存表），用{{c2::仅追加流（append-only）}}；外部表或外部管理的 Iceberg 表，只能用{{c3::仅插入流（insert-only）}}。含地理空间数据的对象，标准流无法取回变更，建议用{{c4::仅追加流}}。
