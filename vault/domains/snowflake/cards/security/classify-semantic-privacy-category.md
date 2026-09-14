---
id: classify-semantic-privacy-category
node: security.data-classification-and-tagging
type: qa
tags: [grown]
---
## Q
Snowflake 的敏感数据分类（data classification）自动分析一张表后，会给列输出哪两个层面的判断？结果最终怎么落地成保护？

## A
分类会采样列的数据和元数据，给出两类判断：语义类别（semantic category，如 EMAIL、PHONE_NUMBER、NAME）与隐私类别（privacy category，如 IDENTIFIER 直接标识符、QUASI_IDENTIFIER 准标识符、SENSITIVE 敏感信息）。结果以系统标签（`SNOWFLAKE.CORE.SEMANTIC_CATEGORY`、`SNOWFLAKE.CORE.PRIVACY_CATEGORY`）的形式打到列上；再把脱敏策略关联到这些标签，就形成“自动发现 → 自动打标签 → 自动脱敏”的链路。
