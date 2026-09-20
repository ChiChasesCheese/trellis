You are putting flashcards in the order a learner should first meet them.

For every topic below you get its cards: id, question, and the start of the
answer. Return the ids of each topic in teaching order. The rules, in order
of precedence:

1. A card that uses a term comes after the card that defines it.
2. What it is → how it works → why it is built that way → where it breaks
   or what it costs → numbers and operations → applying it to a scenario.
3. The plain statement of an idea comes before its edge cases and exceptions.
4. When two cards are independent, the one a practitioner needs more often
   comes first.

Every id of a topic must appear exactly once, under its own topic. Do not
invent, drop, rename or move ids. Output only JSON, in this shape:

{
  "security.protocols-auth-encryption": ["<id shown first>", "…"],
  "security.authorization": ["<id shown first>", "…"],
  "security.audit-hardening": ["<id shown first>", "…"]
}

## security.protocols-auth-encryption — 安全协议、身份验证（SSL/SASL）与加密
掌握SSL与SASL两类身份验证机制的适用场景、重新认证机制，以及传输加密（含端到端加密）如何保护数据。
- `kafka-security-e2e-encryption-why` Q: Kafka 的 SSL/SASL_SSL 传输加密（TLS）已经能防止网络窃听，为什么面对高度敏感数据或 PII（个人身份信息）时，还建议在生产者/消费者的序列化器（serializer）/反序列化器（deserializer）里额外做「端到端加密」？
  A: TLS 只保护数据在网络上传输的过程：消息到达 broker 后会以明文写入磁盘日志，也可能出现在 broker 内存的堆转储里，这意味着拥有磁盘或平台访问权限的管理员（包括云服务商）理论上仍能读到明文内容。端到端加密把加解密下放到客户端：生产者用来自密钥管理系统（KMS，key management system）的
- `kafka-security-e2e-key-rotation-compaction` Q: 端到端加密建议定期轮换用于加解密消息的共享密钥，但为什么这在压实型主题（compacted topic，对每个 key 只保留最新一条消息的主题）上会格外麻烦？
  A: 轮换密钥能降低密钥一旦泄露的影响范围、防止暴力破解，但只要用旧密钥加密的消息还在保留策略内，新旧密钥就必须同时保持可用以便解密。普通主题的旧消息会随时间过期，压实主题却可能长期保留某个 key 下用旧密钥加密的历史消息，等于要长期维护多套密钥，甚至需要用新密钥对旧消息重新加密；而重新加密期间为避免和新写入的消息产生冲突
- `kafka-security-protocol-choice` Q: Kafka broker 在监听器（listener，broker 用来接收客户端连接的网络端点）上可配置 PLAINTEXT、SSL、SASL_PLAINTEXT、SASL_SSL 四种安全协议之一。为什么内部监听器（只有集群内部、受物理保护的机器才能访问）可以用 PLAINTEXT，而暴露在公网的外部监听器绝不能用？
  A: PLAINTEXT 和 SASL_PLAINTEXT 的传输层不加密，数据以明文在网络上传输；SASL_PLAINTEXT 虽然做了身份验证，但认证凭证和之后的消息内容都可能被窃听。只有 SSL 和 SASL_SSL 用 TLS 做传输加密，能防止窃听和篡改。内部监听器所在网络已被物理隔离、只有授权人员可达，即使不加密
- `kafka-security-reauth-mechanism` Q: 客户端用 GSSAPI（Kerberos）或 OAUTHBEARER 这类使用有限生存期凭证的 SASL 机制认证后，broker 的后台登录线程会不断获取新凭证；但一条已经建立好的旧连接，为什么不会自动感知它当初用的凭证已经过期或被撤销？该如何解决？
  A: Kafka 默认只在**建立新连接**时校验凭证：连接一旦通过身份验证，就会在其生命周期内一直沿用当初获得的身份（KafkaPrincipal），直到因超时或网络错误自然断开为止，broker 不会主动去检查这条连接背后的凭证是否已经过期或被吊销。解决办法是给 broker 配置 `connections.max.re
- `kafka-security-sasl-mechanism-choice` Q: Kafka 内置支持 GSSAPI、PLAIN、SCRAM-SHA-256/512、OAUTHBEARER 四种 SASL 机制。已经有企业级 Kerberos 基础设施、不想额外部署密码存储、以及客户端已经用 OAuth 2.0 签发令牌，这三种场景分别该选哪种机制？
  A: 已有 Kerberos（可对接 Active Directory 或 OpenLDAP）基础设施时选 **GSSAPI**，它直接用 Kerberos 票据完成客户端与服务器的双向认证；不想引入额外密码服务器时选 **SCRAM**（SCRAM-SHA-256/512），它把加盐后的哈希密码内置保存在 broker 端
- `kafka-security-sasl-plain-must-use-ssl` Q: 为什么使用 SASL/PLAIN 机制时，必须搭配 SASL_SSL 协议，而不能用不加密的 SASL_PLAINTEXT？
  A: SASL/PLAIN 认证时，客户端会把用户名和密码以明文形式发送给 broker。如果传输层不加密（SASL_PLAINTEXT），网络上的窃听者可以直接截获这些明文凭证，进而冒充合法用户。搭配 SASL_SSL 后，认证过程和之后的所有数据都跑在 TLS 加密通道里，即使被截获也只是密文，凭证不会泄露。这也是为什么
- `kafka-security-ssl-vs-sasl-choice` Q: 要让客户端和 broker 互相验证身份并加密数据，既可以用 SSL 协议（依赖为每个客户端签发的 TLS 证书做双向认证），也可以用 SASL_SSL（TLS 负责加密+服务器认证，SASL 负责客户端认证）。什么情况下应该选 SASL_SSL 而不是纯 SSL 客户端证书认证？
  A: SSL 双向认证要求给每一个客户端签发、分发、定期轮换 TLS 证书，客户端数量一多，证书管理成本就会失控。SASL（simple authentication and security layer，简单身份验证和安全层）把认证逻辑抽成独立机制，可以用用户名密码（PLAIN/SCRAM）、Kerberos 票据（GSS

## security.authorization — 授权：ACL与自定义授权
理解基于ACL的默认授权器如何控制主题、群组等资源的访问权限，以及如何实现自定义授权逻辑。
- `kafka-security-acl-deny-priority` Q: 在同一个资源上，如果既有一条 AllowACL（允许类访问控制列表条目）授权 User:Alice 读取，又有一条 DenyACL（拒绝类访问控制列表条目）禁止 User:Alice 读取，Kafka 内置的 AclAuthorizer 最终会不会放行这次读取？为什么这样设计？
  A: 不会放行。AclAuthorizer 判断是否授权时，Deny 的优先级高于 Allow：只要有一条匹配的 DenyACL，不管有多少条匹配的 AllowACL 都会被拒绝；只有在没有匹配的 DenyACL、且至少有一条匹配的 AllowACL 时才允许访问。这样设计是为了让管理员能用一条精确的 DenyACL 去覆盖
- `kafka-security-acl-fields` Q: 一条 Kafka ACL（access control list，访问控制列表）由七部分组成：{{c1::资源类型（如 Topic、Group、Cluster）}}、{{c2::模式类型（Literal 字面量匹配 或 Prefixed 前缀匹配）}}、{{c3::资源名称（具体名称、前缀，或通配符 * 表示全部）}}、{{c4::操作（如 Read、Write、Create、Delete、Describe 等）}}、{{c5::权限类型（Allow 或 Deny，Deny 优先级更高）}}、{{c6::主体（格式为 `<主体类型>:<主体名称>`，如 User:Alice）}}、{{c7::主机（客户端连接的源 IP，或 * 表示所有主机）}}。
- `kafka-security-allow-everyone-tradeoff` Q: broker 参数 `allow.everyone.if.no.acl.found=true` 会让所有没有配置任何 ACL 的资源默认对所有用户开放。这个开关在什么阶段有用？为什么不建议在生产环境长期开启？
  A: 这个开关在集群第一次启用授权、或开发调试阶段很有用：可以先打开身份验证和授权框架，而不必一次性为所有已有资源都补齐 ACL，避免立刻中断正在使用这些资源的客户端。但生产环境不建议长期开启，原因有二：一是一旦创建了新资源却忘了配置 ACL，它会默认对所有用户开放，造成意外的权限泄露；二是一旦之后给这个资源加上任何前缀或通
- `kafka-security-custom-authorizer-context` Q: 内置的 AclAuthorizer 只按「主体+资源+操作」做静态授权判断。如果想实现「创建/删除 ACL 这类管理请求只能从内部监听器（internal listener，只对可信内网开放的连接入口）发起，外部监听器一律拒绝」这样与连接上下文相关的规则，应该怎么做？
  A: 可以写一个继承 AclAuthorizer 的自定义授权器，重写它的 authorize 方法。Kafka 会把包含监听器名称、安全协议、请求类型等元数据的请求上下文（AuthorizableRequestContext）传给这个方法，自定义逻辑先判断请求类型是否属于要限制的管理操作、且当前连接用的监听器名称不是内部监
- `kafka-security-service-credentials-long-running` Q: 对于长时间运行的应用程序（比如一个常驻后台的消费者服务），为什么建议给它配置独立的「服务凭证」，而不是直接用某个员工的个人账号凭证进行身份验证？
  A: 如果长期运行的服务用的是某个员工的个人身份，一旦这名员工离职、其账号和 ACL 被立即撤销，这个仍在运行的服务也会跟着被中断；而且由于长寿命连接可能在账号被删除之后还能继续处理一段时间的请求，这段时间里系统实际上仍在被一个「已经不该存在」的身份访问，带来安全风险。使用与具体人员无关的服务凭证，能把服务的访问权限生命周期
- `kafka-security-super-users-vs-acl` Q: 授权时既可以把某个主体加进 broker 配置 `super.users`（超级用户，对所有资源拥有不受限制的访问权限）里，也可以用普通 ACL 精确授权同样的资源。为什么生产环境中更推荐用普通 ACL 而不是把用户列为超级用户？
  A: 超级用户对所有资源都有无限制的访问权限，而且不能用 DenyACL 限制它——一旦超级用户的凭证被窃取，攻击者就能访问整个集群；更糟的是，撤销超级用户权限必须把它从 `super.users` 配置里删除并重启所有 broker 才能生效，响应速度很慢。普通 ACL 是按「资源+操作」精确授权的，撤销时只需要删除对应 

## security.audit-hardening — 审计与平台整体加固
掌握审计日志的作用，以及保护ZooKeeper、密码与整体平台安全所需的额外加固手段。
- `kafka-security-audit-log-level-split` Q: Kafka broker 的授权器日志里，一次被拒绝的访问记录在 INFO 级别，一次被允许的访问却只记录在 DEBUG 级别。这样按结果区分日志级别，对安全审计有什么好处？
  A: 生产环境通常默认持续采集 INFO 级别日志，而 DEBUG 级别默认关闭以避免日志量爆炸。把「拒绝访问」这类更值得关注的安全事件放在 INFO 级别，意味着不需要专门为了审计而打开高噪声的 DEBUG 日志，就能持续监控未授权访问尝试（比如某个身份反复访问自己无权限的主题）；而「允许访问」的正常流量数据量巨大，只在排
- `kafka-security-config-provider-no-plaintext-password` Q: 即使已经用文件系统权限限制了谁能读取 broker 或客户端的配置文件，为什么仍然建议不要在配置文件里直接保存明文密码，而要通过 ConfigProvider（配置提供程序）间接加载？
  A: 文件系统权限只能挡住没有对应访问权限的用户，配置文件仍可能因为备份、日志采集、误操作复制等途径被间接暴露；一旦文件内容泄露，里面的明文密码可以被直接拿去用。Kafka 支持配置 ConfigProvider：配置文件里只写一个间接引用，例如 `password=${gpg:/path/to/credentials.pr
- `kafka-security-e2e-audit-header-integrity` Q: 如果想对一条消息做端到端的审计追踪（记录它经过了哪些处理环节），建议把审计元数据放在消息的什么位置？又如何防止这些审计元数据在传输过程中被篡改？
  A: 建议把审计元数据放进消息标头（message header）中，这样审计信息随消息本身一起在整条 Kafka 数据流中流转，不需要额外的旁路系统也能追溯一条消息经过的处理环节。为了防止标头内容在传输或存储中途被篡改，可以使用端到端加密（在生产者、消费者两端加解密，broker 不参与）来保护消息标头的完整性，确保这些审
- `kafka-security-zk-digest-md5-not-for-prod` Q: ZooKeeper 支持用 SASL/DIGEST-MD5 做用户名密码身份验证，但这种方式不适合用在生产环境，为什么？
  A: SASL/DIGEST-MD5 本身存在已知的安全漏洞，而且不会自己加密传输的凭证，如果不叠加额外的传输加密，密码可能被网络窃听截获。即便配合 TLS 加密使用，出于已知漏洞的考虑，生产环境仍应优先选择基于 Kerberos 的 SASL/GSSAPI 身份验证，而不是 SASL/DIGEST-MD5。
- `kafka-security-zk-multi-principal-or-logic` Q: Kafka broker 端的 AclAuthorizer 判断规则是「只要有一条匹配的 DenyACL 就拒绝」，具有更高优先级的收紧效果。但如果给 ZooKeeper 同时启用 SASL 和 SSL 两种协议做客户端身份验证，导致一个连接关联了多个主体（principal），ZooKeeper 的授权判断规则和 Kafka 有什么不同？
  A: ZooKeeper 采用的是更宽松的「或」逻辑：一个连接如果同时通过 SASL 和 SSL 两种方式认证从而关联了多个主体，只要这些主体中**任意一个**对某个资源有访问权限，ZooKeeper 就会授予这次访问，并不存在像 Kafka 的 DenyACL 那样能收紧权限的优先规则。这意味着给 ZooKeeper 同时
- `kafka-security-zk-node-acl-defaults` Q: 给 Kafka broker 配置了 `zookeeper.set.acl=true` 后，ZooKeeper 中保存普通元数据的节点默认是什么访问策略？保存 SCRAM 用户名密码凭证的节点呢？
  A: 普通元数据节点默认是「公开可读、只有 broker 能修改」：任何人都能查看节点内容，但只有 broker 的身份能写入或修改，如果内部管理员想绕过 broker 直接通过 ZooKeeper 客户端改元数据，需要额外配置 ACL 授权给管理员主体。但像保存 SCRAM 密码凭证这类敏感路径，默认是不公开的，防止任何非
