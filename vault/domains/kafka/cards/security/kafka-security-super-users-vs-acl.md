---
id: kafka-security-super-users-vs-acl
node: security.authorization
type: qa
source: kafka-2e
---
## Q
授权时既可以把某个主体加进 broker 配置 `super.users`（超级用户，对所有资源拥有不受限制的访问权限）里，也可以用普通 ACL 精确授权同样的资源。为什么生产环境中更推荐用普通 ACL 而不是把用户列为超级用户？

## A
超级用户对所有资源都有无限制的访问权限，而且不能用 DenyACL 限制它——一旦超级用户的凭证被窃取，攻击者就能访问整个集群；更糟的是，撤销超级用户权限必须把它从 `super.users` 配置里删除并重启所有 broker 才能生效，响应速度很慢。普通 ACL 是按「资源+操作」精确授权的，撤销时只需要删除对应 ACL，就能通过 ZooKeeper 的 watcher 通知机制立刻在所有 broker 上生效，不需要重启，因此凭证一旦泄露能更快地收回权限。
