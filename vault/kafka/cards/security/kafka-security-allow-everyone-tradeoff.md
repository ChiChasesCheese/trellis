---
id: kafka-security-allow-everyone-tradeoff
node: security.authorization
type: qa
source: kafka-2e
---
## Q
broker 参数 `allow.everyone.if.no.acl.found=true` 会让所有没有配置任何 ACL 的资源默认对所有用户开放。这个开关在什么阶段有用？为什么不建议在生产环境长期开启？

## A
这个开关在集群第一次启用授权、或开发调试阶段很有用：可以先打开身份验证和授权框架，而不必一次性为所有已有资源都补齐 ACL，避免立刻中断正在使用这些资源的客户端。但生产环境不建议长期开启，原因有二：一是一旦创建了新资源却忘了配置 ACL，它会默认对所有用户开放，造成意外的权限泄露；二是一旦之后给这个资源加上任何前缀或通配符匹配的 ACL，「没有找到 ACL」这个条件就不再成立，原本靠这个开关默认能访问的用户可能会突然失去访问权限。
