---
id: trust-center-typical-findings
node: security.trust-center-posture
type: qa
tags: [grown]
---
## Q
信任中心（Trust Center）扫描常报出的高优先级安全发现项有哪几类？它们为什么危险？

## A
典型的几类：(1) 人类用户未启用 MFA（多因素认证）或仍用纯密码登录——密码泄露即可直接登录；(2) 账户没有网络策略（network policy）或允许 `0.0.0.0/0`——任意来源都能尝试登录；(3) ACCOUNTADMIN 等高权限角色授予了过多用户，或被设为用户的默认角色——扩大了误操作和被盗用的影响面；(4) 服务账号使用密码而不是密钥对。这些都属于配置层面的错误，不需要漏洞利用就能被攻击者利用。
