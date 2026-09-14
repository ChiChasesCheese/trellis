---
id: security-passkeys-phishing
node: security.authn.credentials
type: qa
---
## Q
Why are passkeys (WebAuthn) phishing-resistant when passwords + TOTP codes are not?

## A
Password and TOTP are **user-typeable secrets** — a fake site can ask for them and relay them to the real site in real time (proxy phishing defeats OTP).

Passkeys sign a **challenge with a device-held private key**, and the browser scopes the credential to the **origin** it was registered on:

- On `evil-bank.com`, the browser simply has no credential for that origin — there is nothing to phish and nothing to relay.
- The private key never leaves the authenticator (or synced keychain), so there's no shared secret on the server to breach — the server stores only public keys.

Per-site keypairs also kill credential reuse/stuffing. This is why 2026 guidance treats passkeys, not SMS/TOTP, as the strong second (or only) factor.

## Q zh
为什么 passkey（WebAuthn）抗钓鱼而密码 + TOTP 码不？

## A zh
密码和 TOTP 是**用户可输入秘密** — 虚假网站可要求它们并实时中继到真实网站（代理钓鱼打败 OTP）。

Passkey 用**设备持有私钥**签署**挑战**，浏览器将凭证范围限定到**注册的 origin**：

- 在 `evil-bank.com` 上，浏览器根本没那个 origin 的凭证 — 无可钓鱼和无可中继。
- 私钥永不离开 authenticator（或同步钥匙链），所以服务端无共享秘密被破坏 — 服务端仅存公钥。

按网站密钥对也杀凭证重用/填充。这是为什么 2026 指导把 passkey（不是 SMS/TOTP）当强二因素（或仅因素）。
