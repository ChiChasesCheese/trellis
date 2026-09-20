---
id: problems-email-service-spf-dkim-dmarc-distinct-proofs
node: problems.media.email-service
type: qa
step: 3
tags: [grown]
---
## Q
In email deliverability design, SPF, DKIM and DMARC are often treated as an interchangeable authentication bundle. What distinct claim does each one actually prove, and why can a phishing email pass both SPF and DKIM while still being caught by DMARC?

## A
SPF proves the connecting server's IP is authorized to send on behalf of the envelope sender domain (the MAIL FROM/HELO domain checked against a DNS-published list) — it says nothing about the From: header the user actually sees. DKIM proves that specific signed headers and the body weren't altered after a domain applied its cryptographic signature — it does require the From: header to be signed, but the specification does not require the signing domain to match any other identifier, so a signature can be entirely valid while signing for a different domain than the one displayed. DMARC is the piece that closes this gap: it requires the domain verified by SPF or DKIM to be *aligned* with the visible From: header domain. A phishing email can pass SPF and DKIM cleanly by registering its own fresh domain and configuring both correctly for that domain — it only fails DMARC if the attacker's domain doesn't align with whatever domain it's impersonating in the From: header, which is exactly the identity check SPF and DKIM alone don't perform.

## Q zh
在邮件可送达性设计中，SPF、DKIM、DMARC 经常被当作一个可互换的认证组合。这三者各自真正证明的是什么不同的命题？为什么一封钓鱼邮件可以同时通过 SPF 和 DKIM，却仍然被 DMARC 拦下？

## A zh
SPF 证明的是「连接发信的服务器 IP 有权代表信封发件人域名发信」（检查的是 MAIL FROM/HELO 域名对照 DNS 里发布的授权列表）——它对用户实际看到的 From: 头只字未提。DKIM 证明的是「某些被签名的头部和正文，在域名签名之后没有被篡改」——规范确实要求 From: 头必须被签名，但并不要求签名域名和其他任何身份字段一致，所以一个完全有效的签名完全可能是为一个和显示域名不同的域名签的。DMARC 正是填上这个空当的一环：它要求 SPF 或 DKIM 验证通过的域名，必须和用户看到的 From: 头域名「对齐」。一封钓鱼邮件可以通过注册自己全新的域名、并为这个域名正确配置 SPF 和 DKIM，从而干净地通过这两项检查——它只会在攻击者的域名和它在 From: 头里冒充的域名不对齐时被 DMARC 拦下，而这恰恰是 SPF 和 DKIM 单独都没有做的身份核对。
