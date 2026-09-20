---
nodes: [problems.media.email-service]
url: https://www.rfc-editor.org/rfc/rfc9051
---
# RFC 9051 — Internet Message Access Protocol (IMAP) — Version 4rev2
值得读：定义了 UID/UIDVALIDITY、系统 flag（`\Seen` 等）和 `IDLE` 常连接推送机制
的权威模型。本题解「核心实体与 API」的 MailboxEntry 呼应了它的 flag 设计（可变
状态与消息内容分离），「深入探讨」第 7 节的 IMAP `IDLE` 常连接通道直接对应这份
RFC 定义的推送机制。
