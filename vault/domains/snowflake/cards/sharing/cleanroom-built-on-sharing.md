---
id: cleanroom-built-on-sharing
node: sharing.clean-rooms-privacy
type: qa
tags: [grown]
---
## Q
Snowflake 数据洁净室（Data Clean Room）底层是否需要把双方数据复制到一个第三方中立环境里？这对成本和数据新鲜度意味着什么？

## A
不需要。Snowflake 洁净室构建在安全数据共享（Secure Data Sharing）和平台内的策略控制之上：双方数据仍在各自账户的存储中，通过共享授权和受批准的查询在平台内计算，无需搬运数据到第三方。因此没有额外的数据复制和 ETL 管道，查询基于双方的实时数据；代价是双方都需要在 Snowflake 上（或使用洁净室提供的托管方式），并由分析执行方承担计算费用。
