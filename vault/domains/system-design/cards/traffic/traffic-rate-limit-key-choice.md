---
id: traffic-rate-limit-key-choice
node: traffic.rate-limiting
type: qa
---
## Q
What key do you rate limit on — and what goes wrong with per-IP limits?

## A
Primary: the **authenticated principal** (API key / user id) — the unit quotas and billing are written against. Per-IP is the fallback for unauthenticated endpoints (login, signup) but fails both ways: CGNAT puts thousands of legitimate users behind one IP (false positives), while botnets spread across thousands of IPs (false negatives).

Production layers several: a global limit protecting infrastructure, per-principal limits for fairness, and per-endpoint limits weighted by cost — expensive operations (search, export) may count units of work, not requests.

## Q zh
你对什么键进行速率限制 — 每 IP 限制会出什么问题？

## A zh
主要：**认证的主体**（API 密钥/用户 id）— 配额和计费写的单位。每 IP 是未认证端点（登录、注册）的后备，但两种方式都失败：CGNAT 在一个 IP 后放置数千个合法用户（假正），而僵尸网络跨数千个 IP（假负）。

生产层多个：保护基础设施的全局限制、每主体限制以实现公平性，以及按成本加权的每端点限制 — 昂贵操作（搜索、导出）可能计数工作单位，而不是请求。
