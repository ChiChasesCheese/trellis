---
id: problems-auth-service-hashing-cost-cores
node: problems.foundations.auth-service
type: qa
step: 1
tags: [grown]
---
## Q
In an authentication service tuning Argon2id to ~150ms per password verify, with a peak login rate of ~434 QPS, roughly how many CPU cores does the password-verification tier need, and why does this number matter?

## A
One core does about 1000ms/150ms ≈ 6.7 verifies/sec, so covering a 434 QPS peak needs about 434/6.7 ≈ 65 cores, or roughly 130 with 2x headroom for bursts and failover. The number matters because password hashing is deliberately expensive (that's the point of a memory-hard KDF), so the work-factor choice is not just a security knob — it's a capacity-planning input. Any time the hash parameters are tuned upward for security, this core count must be recomputed rather than assumed to still fit the existing fleet.

## Q zh
在一个把 Argon2id 调到约 150ms/次验证、峰值登录约 434 QPS 的认证服务中，密码验证层大致需要多少 CPU 核心，为什么这个数字重要？

## A zh
一个核心大约能做 1000ms/150ms ≈ 6.7 次验证/秒，所以覆盖 434 QPS 峰值需要约 434/6.7 ≈ 65 核，含 2 倍冗余约 130 核。这个数字重要是因为密码哈希故意做得很慢（这正是内存硬 KDF 的意义所在），所以工作因子的选择不只是安全旋钮——它是容量规划的输入。任何时候把哈希参数调高以换取安全性，都必须重新计算这个核心数，而不是假设现有资源池还够用。
