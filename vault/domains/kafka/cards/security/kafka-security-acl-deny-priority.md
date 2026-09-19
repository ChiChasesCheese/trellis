---
id: kafka-security-acl-deny-priority
node: security.authorization
type: qa
step: 2
source: kafka-2e
---
## Q
在同一个资源上，如果既有一条 AllowACL（允许类访问控制列表条目）授权 User:Alice 读取，又有一条 DenyACL（拒绝类访问控制列表条目）禁止 User:Alice 读取，Kafka 内置的 AclAuthorizer 最终会不会放行这次读取？为什么这样设计？

## A
不会放行。AclAuthorizer 判断是否授权时，Deny 的优先级高于 Allow：只要有一条匹配的 DenyACL，不管有多少条匹配的 AllowACL 都会被拒绝；只有在没有匹配的 DenyACL、且至少有一条匹配的 AllowACL 时才允许访问。这样设计是为了让管理员能用一条精确的 DenyACL 去覆盖已有的、范围更宽的通配符或前缀 AllowACL，方便在不动原有大范围授权规则的情况下临时收紧某个主体的权限。
