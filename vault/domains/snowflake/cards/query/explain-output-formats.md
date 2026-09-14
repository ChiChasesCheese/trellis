---
id: explain-output-formats
node: query.explain-plan-interpretation
type: cloze
tags: [grown]
---
Snowflake 的 `EXPLAIN USING {{c1::TABULAR}} | {{c2::JSON}} | {{c3::TEXT}} <语句>` 以三种格式之一输出执行计划，默认是 {{c1::TABULAR}}（表格）；以 JSON 格式得到的计划可用 {{c4::SYSTEM$EXPLAIN_JSON_TO_TEXT}} 转成易读的文本。
