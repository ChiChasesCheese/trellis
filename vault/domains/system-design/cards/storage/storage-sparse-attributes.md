---
id: storage-sparse-attributes
node: storage.record-modeling
type: qa
---
## Q
Products in your catalog have wildly different attributes (screen size, shoe size, caffeine content…). Compare the three standard ways to store heterogeneous sparse attributes — wide table, EAV, JSON column — on querying, indexing, and validation.

## A
- **Wide table** (a column per attribute, mostly NULL): full SQL typing, constraints, and per-column indexes — but every new attribute is a DDL change, and hundreds of mostly-null columns rot the schema. Fine only when the attribute set is small and stable.
- **EAV** (entity–attribute–value rows: `product_id, attr_name, attr_value`): attributes appear without DDL, but values collapse to one stringly-typed column (no type checks, no cross-attribute constraints), reassembling one product means pivoting many rows, and "screen > 15 AND weight < 2" becomes self-join soup that optimizers estimate badly. Largely an anti-pattern today.
- **JSON column** (`jsonb` beside the typed core columns): one read returns the whole record; a **GIN index** covers ad-hoc containment queries, and an expression index can target a hot key (`(attrs->>'brand')`). Costs: the database validates nothing inside the blob (schema-on-read — enforce with app-level schemas or CHECK constraints), and in Postgres updating one key rewrites the whole value.

Default today: typed columns for the attributes everything shares and you filter on constantly; JSON for the sparse long tail.

## Q zh
你目录里的商品属性五花八门（屏幕尺寸、鞋码、咖啡因含量……）。就查询、索引、校验三方面，比较存储异构稀疏属性的三种标准方式 — 宽表、EAV、JSON 列。

## A zh
- **宽表**（每个属性一列，大多为 NULL）：完整的 SQL 类型、约束和按列索引 — 但每个新属性都是一次 DDL 变更，几百个几乎全空的列会让 schema 腐烂。只在属性集小而稳定时合适。
- **EAV**（entity–attribute–value 行：`product_id, attr_name, attr_value`）：新属性不需要 DDL，但值都塌缩进一个字符串型的列（没有类型检查、没有跨属性约束），拼回一个商品要透视很多行，而"screen > 15 AND weight < 2"变成一锅自 join 汤，优化器对它的估算很糟。如今基本被视为反模式。
- **JSON 列**（在有类型的核心列旁放一个 `jsonb`）：一次读取返回整条记录；**GIN 索引**覆盖临时的包含（containment）查询，expression index 可以瞄准热点 key（`(attrs->>'brand')`）。代价：数据库对 blob 内部不做任何校验（schema-on-read — 用应用层 schema 或 CHECK 约束来兜底），而且在 Postgres 里更新一个 key 要重写整个值。

当下的默认做法：所有商品共有、且你频繁过滤的属性用有类型的列；稀疏的长尾放 JSON。
