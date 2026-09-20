---
nodes: [problems.media.email-service]
url: https://www.rfc-editor.org/rfc/rfc6376
---
# RFC 6376 — DomainKeys Identified Mail (DKIM) Signatures
值得读：DKIM 要求签名必须覆盖 `From:` 头（比 SPF 更强），但规范原文明确签名域名
不要求和其他头字段里的身份一致——这正是本题解「深入探讨」第 2 节里"DKIM 通过不
代表签名域名等于用户看到的域名"这一结论的直接依据，也是 DMARC 存在的理由之一。
