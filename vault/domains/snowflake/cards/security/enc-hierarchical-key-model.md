---
id: enc-hierarchical-key-model
node: security.encryption-key-hierarchy
type: cloze
tags: [grown]
---
Snowflake 的分层密钥模型（hierarchical key model）自上而下为：{{c1::根密钥（root key，保存在云厂商的硬件安全模块 HSM 中）}} → {{c2::账户主密钥（account master key）}} → {{c3::表主密钥（table master key）}} → {{c4::文件密钥（file key，加密单个数据文件）}}。每一层密钥只用来加密（包装）下一层的密钥。
