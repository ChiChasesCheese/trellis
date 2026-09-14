---
id: kafka-security-config-provider-no-plaintext-password
node: security.audit-hardening
type: qa
source: kafka-2e
---
## Q
即使已经用文件系统权限限制了谁能读取 broker 或客户端的配置文件，为什么仍然建议不要在配置文件里直接保存明文密码，而要通过 ConfigProvider（配置提供程序）间接加载？

## A
文件系统权限只能挡住没有对应访问权限的用户，配置文件仍可能因为备份、日志采集、误操作复制等途径被间接暴露；一旦文件内容泄露，里面的明文密码可以被直接拿去用。Kafka 支持配置 ConfigProvider：配置文件里只写一个间接引用，例如 `password=${gpg:/path/to/credentials.props.gpg:password}`，运行时由 ConfigProvider 从外部安全存储或用 gpg 等工具解密加密文件后动态注入真实密码。这样磁盘和版本控制中都不会出现明文密码本身，即使配置文件泄露，攻击者拿到的也只是密文和一个引用路径。
