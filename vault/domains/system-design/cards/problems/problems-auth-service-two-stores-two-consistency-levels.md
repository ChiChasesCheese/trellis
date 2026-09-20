---
id: problems-auth-service-two-stores-two-consistency-levels
node: problems.foundations.auth-service
type: qa
step: 3
tags: [grown]
---
## Q
In an authentication service, why should refresh-token storage and the core credential-of-record (password hash, account lock status) live in two physically separate stores with different consistency levels, rather than one?

## A
The write volumes differ by roughly four orders of magnitude: core credential writes (signup, password change, lockout) run at only a few QPS even at scale, while refresh-token rotation writes can peak in the tens of thousands per second. The credential-of-record can afford strong, single-leader cross-region consistency because its write volume is tiny — and it needs that strength, since a stale read of a lockout or password change is a security hole. The refresh-token store needs to be sharded for throughput and only needs consistency within one token family, not globally, so forcing it onto the same strongly-consistent store would apply a throughput ceiling it can't meet; forcing the credential store onto the refresh store's weaker, sharded model would open a window where a password change hasn't propagated everywhere yet.

## Q zh
在认证服务中，为什么 refresh token 存储和核心凭证记录（密码哈希、账号锁定状态）应该存在两套物理独立、一致性级别不同的存储里，而不是一套？

## A zh
两者写量相差约四个数量级：核心凭证写入（注册、改密码、锁定）即使在大规模下也只有每秒几次，而 refresh token 轮换写入峰值可达每秒数万次。核心凭证记录可以承受强一致的单主跨区域复制,因为它的写量很小——而且它需要这种强度,因为读到陈旧的锁定或改密码状态就是安全漏洞。refresh token 存储需要为吞吐分片,只需要单个 token family 内部一致,不需要全局一致,所以强行放进同一个强一致存储会带来它扛不住的吞吐上限；反过来把凭证存储放进 refresh 存储更弱的分片模型,会打开一个密码修改尚未全局生效的窗口。
