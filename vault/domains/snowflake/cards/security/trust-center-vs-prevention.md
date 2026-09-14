---
id: trust-center-vs-prevention
node: security.trust-center-posture
type: qa
tags: [grown]
---
## Q
开启了信任中心（Trust Center）扫描，是否就意味着账户的这些安全风险被自动阻止了？它和网络策略、认证策略这类控制的关系是什么？

## A
不是。信任中心是检测性（detective）控制：它发现并报告错误配置、给出修复建议，但本身不改变配置、不拦截登录或查询。真正阻止访问的是预防性（preventive）控制，如网络策略、认证策略（强制 MFA）、RBAC 授权。正确用法是用信任中心持续发现偏离基线的配置，再由管理员去修改相应的预防性控制，并在下次扫描中确认发现项消失。
