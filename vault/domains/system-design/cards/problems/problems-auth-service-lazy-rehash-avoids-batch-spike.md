---
id: problems-auth-service-lazy-rehash-avoids-batch-spike
node: problems.foundations.auth-service
type: qa
step: 8
tags: [grown]
---
## Q
In an authentication service with hundreds of millions of existing password hashes, how do you migrate everyone to stronger hashing parameters without creating a one-time spike on the hashing tier?

## A
You cannot batch-rehash offline, because a one-way hash cannot be recomputed with new parameters without the plaintext password. Instead, use lazy re-hashing: on each successful login, after verifying against the old parameters, re-hash the password with the new parameters and overwrite the stored value. Migration load is then spread across real login traffic over time — proportional to how often each account actually logs in — instead of being concentrated into a single batch job that would need to be sized for the entire account base at once.

## Q zh
在一个已有数亿密码哈希的认证服务中，怎样把所有用户迁移到更强的哈希参数，同时不在哈希层制造一次性峰值？

## A zh
不能离线批量重哈希，因为单向哈希在没有明文密码的情况下无法用新参数重新计算。应该用惰性重哈希（lazy re-hashing）：每次登录成功后，先用旧参数验证通过，再用新参数重新哈希密码并覆盖存储的值。迁移负载随真实登录流量分摊在时间上——和每个账号实际登录的频率成正比——而不是集中成一个需要一次性覆盖全部账号规模的批处理任务。
