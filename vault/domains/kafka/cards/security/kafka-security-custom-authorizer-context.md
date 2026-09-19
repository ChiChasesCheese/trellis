---
id: kafka-security-custom-authorizer-context
node: security.authorization
type: qa
step: 5
source: kafka-2e
---
## Q
内置的 AclAuthorizer 只按「主体+资源+操作」做静态授权判断。如果想实现「创建/删除 ACL 这类管理请求只能从内部监听器（internal listener，只对可信内网开放的连接入口）发起，外部监听器一律拒绝」这样与连接上下文相关的规则，应该怎么做？

## A
可以写一个继承 AclAuthorizer 的自定义授权器，重写它的 authorize 方法。Kafka 会把包含监听器名称、安全协议、请求类型等元数据的请求上下文（AuthorizableRequestContext）传给这个方法，自定义逻辑先判断请求类型是否属于要限制的管理操作、且当前连接用的监听器名称不是内部监听器，两者同时成立就直接返回拒绝（DENIED），否则调用父类的 super.authorize 走原本的 ACL 判断。这利用了 Kafka 授权器可插拔、且能拿到连接级上下文信息的特点，在静态 ACL 之外叠加了基于连接来源的额外访问控制。
