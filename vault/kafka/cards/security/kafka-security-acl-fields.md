---
id: kafka-security-acl-fields
node: security.authorization
type: cloze
source: kafka-2e
---
一条 Kafka ACL（access control list，访问控制列表）由七部分组成：{{c1::资源类型（如 Topic、Group、Cluster）}}、{{c2::模式类型（Literal 字面量匹配 或 Prefixed 前缀匹配）}}、{{c3::资源名称（具体名称、前缀，或通配符 * 表示全部）}}、{{c4::操作（如 Read、Write、Create、Delete、Describe 等）}}、{{c5::权限类型（Allow 或 Deny，Deny 优先级更高）}}、{{c6::主体（格式为 `<主体类型>:<主体名称>`，如 User:Alice）}}、{{c7::主机（客户端连接的源 IP，或 * 表示所有主机）}}。
