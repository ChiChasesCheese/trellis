---
id: problems-auth-service-recovery-shares-rate-limiting
node: problems.foundations.auth-service
type: qa
step: 9
tags: [grown]
---
## Q
In an authentication service, why should the account-recovery endpoint sit behind the same rate-limiting infrastructure as the login endpoint, rather than a separate, more lenient policy?

## A
An attacker running recovery attempts across a large number of accounts (each attempt trying to trigger a password reset or bypass a lost-device flow) has the same traffic signature as credential stuffing against login — low volume per account, spread across many accounts. If recovery isn't covered by the same per-account, per-IP, and global fleet-level rate limiting used for login, it becomes the easier side door: an attacker never needs to break the hardened login path when the recovery path checks less. Recovery is only as strong as its weakest gate, and rate limiting is one of those gates, not an afterthought specific to login.

## Q zh
在认证服务中，为什么账号恢复端点应该和登录端点共用同一套限流基础设施，而不是一套更宽松的独立策略？

## A zh
攻击者对大量账号发起恢复尝试（每次尝试触发密码重置或绕过丢失设备流程）和撞库攻击登录端点有同样的流量特征——每账号低频次、分散在大量账号上。如果恢复流程不受登录所用的按账号、按 IP、全局舰队级限流覆盖，它就会成为更容易的侧门：当恢复路径检查更少时，攻击者根本不需要攻破被加固过的登录路径。账号恢复的强度取决于它最弱的一道关卡，限流是其中一道，不是只属于登录、可以事后补的东西。
