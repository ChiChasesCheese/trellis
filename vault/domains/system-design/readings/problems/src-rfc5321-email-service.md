---
nodes: [problems.media.email-service]
url: https://www.rfc-editor.org/rfc/rfc5321
---
# RFC 5321 — Simple Mail Transfer Protocol
值得读：SMTP 协议本身的权威定义，最关键的是"一旦返回 250，投递责任从发送方转移到
接收方"这条一跳责任转移语义，以及信封（`MAIL FROM`/`RCPT TO`）与消息头是两回事。
本题解「深入探讨」第 1 节的按目的域名分队列重试设计、以及"入站不可用不等于邮件
丢失"这个结论都直接建立在这条规则上；具体的重试时间表 RFC 没有规定，是本题解自己
的假设。
