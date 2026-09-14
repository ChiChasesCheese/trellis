---
id: qas-default-scale-factor
node: pruning.query-acceleration-service
type: cloze
source: snowflake-docs
---
查询加速服务（Query Acceleration Service）的默认最大扩展系数（scale factor）：显式设置 `ENABLE_QUERY_ACCELERATION = TRUE` 时为 {{c1::8}}；在 Gen2 标准仓库或多集群仓库（multi-cluster warehouse）上被自动启用时为 {{c2::2}}；设为 {{c3::0}} 表示不设上限。
