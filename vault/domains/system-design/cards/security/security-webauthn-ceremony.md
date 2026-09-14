---
id: security-webauthn-ceremony
node: security.authn.credentials
type: qa
---
## Q
At a systems level: what does your server store per passkey, and what must it verify on each login ceremony?

## A
**Registration** — server issues a random **challenge**; the authenticator generates a keypair scoped to your **RP ID** and returns the public key. You persist: `credential_id`, `public_key`, `user_handle` (an opaque per-user id, not the email), sign counter, and transports. Attestation is usually `none` for consumer passkeys — you're not verifying the hardware model.

**Authentication** — server issues a fresh challenge; the authenticator signs `authenticatorData || SHA-256(clientDataJSON)`. The server verifies:
- Signature against the **stored public key** for that `credential_id`.
- `challenge` matches the one it just issued and is **single-use** (this is the replay defense).
- `origin` in clientDataJSON is an expected origin, and the `rpIdHash` matches your RP ID.
- **UP** (user present) and, for passwordless/step-up, **UV** (user verified) flags are set.

Two design consequences: the **RP ID is baked into every credential** — it must be a registrable domain suffix (`example.com`, not `app.example.com`) or a later domain change invalidates every passkey; and with **synced** passkeys the sign counter stays 0, so clone detection via counter regression is effectively gone. Store multiple credentials per user — the credential, not the user, is the unit of enrollment and revocation.

## Q zh
在系统级：你的服务器每个 passkey 存什么，每个登录仪式上必须验证什么？

## A zh
**注册** — 服务器发随机**挑战**；authenticator 生成范围限定到你的**RP ID**的密钥对，返回公钥。你持久化：`credential_id`、`public_key`、`user_handle`（不透明按用户 id，不是邮件）、签名计数器和传输。证明通常对消费 passkey 是 `none` — 你不验证硬件模型。

**认证** — 服务器发新挑战；authenticator 签署 `authenticatorData || SHA-256(clientDataJSON)`。服务器验证：
- 针对那个 `credential_id` 的**存储公钥**的签名。
- `challenge` 匹配它刚发的，**单次使用**（这是重放防御）。
- clientDataJSON 中的 `origin` 是期望 origin，`rpIdHash` 匹配你的 RP ID。
- **UP**（用户存在）和，对无密码/升级，**UV**（用户验证）标志被设置。

两个设计后果：**RP ID 烤到每个凭证** — 它必须是可注册域后缀（`example.com`，不 `app.example.com`）或稍后域名改变使每个 passkey 失效；对**同步** passkey 符号计数器停留 0，所以通过计数器回归克隆检测有效地消失。存多个凭证每用户 — 凭证，不是用户，是注册和撤销单位。
