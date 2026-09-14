---
id: enc-tri-secret-secure
node: security.encryption-key-hierarchy
type: qa
tags: [grown]
---
## Q
Tri-Secret Secure（三方密钥保护）在 Snowflake 的密钥层级上加了什么？客户撤销自己的密钥后会发生什么？

## A
Tri-Secret Secure（Business Critical 版本功能）让客户在自己的云 KMS 中持有一把客户管理密钥（CMK，customer-managed key），并与 Snowflake 维护的密钥组合成一把复合主密钥来保护账户数据。任何一方都无法单独解密数据。若客户在 KMS 中禁用或撤销 CMK，Snowflake 就无法再解密该账户的数据，数据实际上变得不可读——这给了客户一个“拔插头”的控制权，代价是密钥运维失误也会导致自身服务不可用。
