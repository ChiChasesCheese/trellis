---
id: enc-transparent-end-to-end
node: security.encryption-key-hierarchy
type: qa
tags: [grown]
---
## Q
Snowflake 客户需要自己为表或 stage 配置加密吗？从客户端上传文件到数据落入表中，数据在哪些环节是加密的？

## A
不需要，加密默认开启且对用户透明，没有“关闭加密”的选项。端到端加密（end-to-end encryption）中：客户端与 Snowflake 之间走 TLS；上传到内部 stage 的文件在落盘前被加密；表中的微分区数据文件用 AES-256 加密后存入对象存储，密钥由分层密钥体系管理。因此即使有人直接拿到底层对象存储里的文件，没有密钥也无法读取。
