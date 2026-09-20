---
id: problems-auth-service-stuffing-fleet-signals-not-lockout
node: problems.foundations.auth-service
type: qa
step: 5
tags: [grown]
---
## Q
In an authentication service under a credential-stuffing attack, why does per-account lockout barely help, and what should the login endpoint rely on instead?

## A
Credential stuffing replays leaked username+password pairs across millions of distinct accounts, typically only one or two attempts per account — it never accumulates enough failures on any single account to trip a per-account lockout, and locking accounts after N failures can even be weaponized against real users (an attacker deliberately fails a victim's login to lock them out — a denial-of-service). The defense that actually works is fleet-level signals: a sudden shift in the global login failure ratio, one IP/ASN/device fingerprint touching thousands of distinct usernames, combined with rate limits applied per account, per IP, and per ASN simultaneously, plus risk-based step-up (require MFA on a new device/geo) rather than an outright block.

## Q zh
在遭受撞库攻击的认证服务中，为什么按账号锁定帮助不大，登录端点应该依赖什么？

## A zh
撞库攻击在数百万个不同账号上重放泄露的用户名+密码对，通常每个账号只尝试一两次——它从不会在任何单个账号上积累到触发按账号锁定所需的失败次数,而且 N 次失败后锁定账号甚至可能被武器化针对真实用户（攻击者故意让受害者的登录失败几次使其被锁定——一种拒绝服务）。真正有效的防御是舰队级信号：全局登录失败率的突然转变、一个 IP/ASN/设备指纹触及数千个不同用户名，配合同时按账号、IP、ASN 三个维度的限流，再加上基于风险的升级（新设备/地理要求 MFA）而不是直接封锁。
