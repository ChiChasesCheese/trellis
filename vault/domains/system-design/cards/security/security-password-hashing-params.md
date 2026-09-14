---
id: security-password-hashing-params
node: security.authn.credentials
type: qa
---
## Q
You must store user passwords and also verify high-entropy API keys. Which algorithm and parameters for each, and why are they different?

## A
**Passwords — a slow, memory-hard KDF.** Argon2id is the default (OWASP baseline ~19 MiB memory, t=2, p=1); bcrypt cost ≥ 12 is acceptable legacy (watch its 72-byte input truncation); scrypt if Argon2 is unavailable. Tune parameters to ~**100–250 ms** per verify on your hardware, then sanity-check that against peak login QPS — password hashing is a deliberate CPU cost and a login stampede can saturate the fleet.

Why: human passwords have maybe 20–30 bits of entropy, so the only defense after a DB leak is making each guess expensive. **Memory-hardness** is the point — it denies GPUs/ASICs the parallelism that lets them do billions of SHA-256/s.

**API keys, session tokens — plain SHA-256 is correct.** A 128-bit random secret is unguessable by brute force, so a slow KDF buys nothing and would add 100 ms to *every API request*. Store the hash, show the key once.

Also: a **per-user salt** (already inside the modular hash string) defeats rainbow tables and shared-password detection; an optional **pepper** held in a KMS/HSM — not in the DB — makes a database-only leak useless.

## Q zh
你必须存储用户密码也验证高 entropy API key。各用什么算法和参数，为什么不同？

## A zh
**密码 — 慢、内存硬 KDF。** Argon2id 是默认（OWASP 基线 ~19 MiB 内存，t=2，p=1）；bcrypt cost ≥12 是可接受的遗留（看它的 72 字节输入截断）；如 Argon2 无可用 scrypt。调参数到你硬件上 ~**100-250 ms** 每验证，然后理智检查对峰值登录 QPS — 密码哈希是刻意 CPU 成本，登录冲击可饱和舰队。

为什么：人类密码也许 20-30 位 entropy，所以 DB 泄漏后唯一防御是让每个猜测成本高。**内存硬度**是要点 — 它拒绝 GPU/ASIC 让他们做数十亿 SHA-256/s 的并行性。

**API key、会话 token — 纯 SHA-256 是正确。** 128 位随机秘密对暴力无法猜测，所以慢 KDF 买不到什么且会加 100 ms 到*每个 API 请求*。存哈希，显示 key 一次。

也：**按用户 salt**（已在模块化哈希字符串内）击败彩虹表和共享密码检测；可选**pepper** 持有在 KMS/HSM — 不在 DB — 让仅数据库泄漏无用。
