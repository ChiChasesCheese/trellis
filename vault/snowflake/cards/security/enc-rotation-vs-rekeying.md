---
id: enc-rotation-vs-rekeying
node: security.encryption-key-hierarchy
type: qa
tags: [grown]
---
## Q
Snowflake 的密钥轮换（key rotation）与定期重新加密（periodic rekeying）有什么区别？各自解决什么问题？

## A
密钥轮换：活跃密钥定期（约每 30 天）退役，新数据改用新密钥加密；退役密钥只用于解密旧数据，不再加密新数据，从而限制单把密钥的使用时长。定期重新加密（rekeying，Enterprise 及以上版本可开启）：对超过一定年限（一年）的旧密钥所加密的数据，后台用新密钥重新加密，之后旧密钥被销毁，使得老数据也不会一直依赖一把老密钥。两者都在后台自动完成，对用户透明、不影响在线查询。
