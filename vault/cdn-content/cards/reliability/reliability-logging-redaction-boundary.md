---
id: reliability-logging-redaction-boundary
node: reliability.logging
type: qa
---
## Q
Debugging a suspected cache leak seems to require logging `Authorization`, cookies, and signed URLs. What is the safe diagnostic design?

## A
Never log raw credentials or signed query values. Log presence, policy decision, bounded classifications, and keyed hashes only when correlation is necessary; redact before serialization, not downstream. Restrict access and retention, test redaction with representative headers, and provide a short-lived privileged capture path only if normal telemetry cannot answer the incident question.

## Q zh
调试疑似 cache leak 似乎需要记录 `Authorization`、cookie 和 signed URL。安全的 diagnostic design 是什么？

## A zh
绝不能记录 raw credential 或 signed query value。只记录 presence、policy decision、bounded classification；需要 correlation 时才记录 keyed hash，并且在 serialization 前完成 redact，而不是依赖 downstream。限制 access 和 retention，用 representative header 测试 redaction；只有普通 telemetry 无法回答 incident question 时，才提供 short-lived privileged capture path。
