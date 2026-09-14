---
id: security-account-recovery
node: security.authn.credentials
type: qa
---
## Q
You ship passkey-only login. Why is your account's real security level probably still "SMS", and how do you design recovery?

## A
An account is only as strong as its **weakest path to a session**. Attackers don't break the passkey — they run the "lost my device" flow. If recovery is an emailed magic link, an SMS code (SIM swap), or a helpdesk call, that becomes the actual authentication mechanism, and the strong factor is decoration.

Design:
- **Prefer re-enrollment over reset**: register **≥2 passkeys** at signup (phone + laptop/security key) and issue single-use **recovery codes** shown once, hashed at rest. Recovery is then "authenticate with your other credential", not "prove you own an inbox".
- Make the fallback path **slow and loud**: a delay (hours to days) with notification to every registered channel and a cancel link, so the legitimate owner can veto. Attackers need silence and speed.
- **On successful recovery, revoke everything**: all sessions, refresh tokens, and API keys — and hold high-risk actions (payouts, changing recovery contacts) behind a cool-down.
- **Helpdesk is an attack surface** (the vector behind several 2023–2025 breaches): require verified, out-of-band identity proof; never let an agent enroll a factor on a caller's say-so.
- No knowledge-based questions — mother's maiden name is public data, not a secret.

## Q zh
你只有 passkey 登录。为什么你账户的真实安全级别可能仍然是「SMS」，怎样设计恢复？

## A zh
账户只与其**到会话的最弱路径**一样强。攻击者不破解 passkey — 他们跑「丢失设备」流程。如果恢复是邮件魔法链接、SMS 码（SIM swap）或帮助台呼叫，那就变成实际认证机制，强因素是装饰。

设计：
- **优先重新注册而不重置**：注册时注册**≥2 个 passkey**（电话 + 笔记本/安全钥匙），发单次**恢复码**显示一次，哈希静止。恢复然后是「用你的其他凭证认证」，不是「证明你拥有收件箱」。
- 让回退路径**慢且大声**：延迟（小时到天），通知所有已注册渠道和取消链接，让合法所有者可否决。攻击者需要沉默和速度。
- **成功恢复时，撤销一切**：所有会话、refresh token 和 API key — 并在冷却期后面放高风险操作（支出、改变恢复联系）。
- **帮助台是攻击面**（2023-2025 几个漏洞的向量）：需验证的、非正式身份证明；绝不让代理基于来电者的口头话语注册因素。
- 无知识型问题 — 母亲的婚前姓是公开数据，不是秘密。
