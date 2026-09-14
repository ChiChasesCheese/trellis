---
id: security-credential-stuffing
node: security.authn.credentials
type: qa
---
## Q
Credential stuffing vs brute force: why does per-account rate limiting barely help, and what actually detects it?

## A
Brute force is *many guesses against one account*; **stuffing replays leaked username+password pairs across millions of accounts** — typically **one or two attempts per account**, from a large residential proxy pool. It never trips a per-account limiter, and the passwords are correct, so hashing cost doesn't matter either.

What detects and blocks it:
- **Fleet-level signals, not per-request ones**: a sudden shift in the global login **failure ratio**, one client/ASN touching thousands of distinct usernames, or unusual success clustering. Rate-limit per IP **and** per ASN/fingerprint **and** globally per endpoint.
- **Breached-credential screening** at signup, login, and password change (HIBP k-anonymity range API — you send 5 hash chars, never the password).
- **Risk-based step-up**: new device/IP/geo → require the second factor or an email confirmation, rather than blocking outright.
- **Passkeys / WebAuthn** remove the attack class entirely — there is no reusable shared secret to replay.

Avoid: locking accounts after N failures (turns stuffing into a **DoS against your users**), and relying on CAPTCHA alone (solver farms cost cents per thousand).

## Q zh
凭证填充 vs 暴力破解：为什么按账户速率限制帮助不大，什么实际检测？

## A zh
暴力是*许多猜测对一个账户*；**填充在百万账户跨重放泄露的用户名+密码对** — 通常**每账户一两次尝试**，来自大型住宅代理池。它从不触发按账户限制器，密码正确，所以哈希成本也不重要。

什么检测和阻止：
- **舰队级信号，不是按请求**：全局登录**失败率**的突然转变，一个客户/ASN 触及数千个不同用户名，或不寻常的成功聚集。按 IP **和**按 ASN/指纹**和**全局按端点速率限制。
- **泄露凭证筛查**在注册、登录和密码改变（HIBP k-anonymity 范围 API — 你发 5 哈希字符，绝不密码）。
- **基于风险的升级**：新设备/IP/地理 → 需第二因素或邮件确认，而不是直接阻止。
- **Passkey / WebAuthn** 完全移除攻击类 — 无可重用共享秘密重放。

避免：N 次失败后锁定账户（把填充变成针对你用户的 **DoS**），仅依赖 CAPTCHA（求解器农场每千次成本几美分）。
