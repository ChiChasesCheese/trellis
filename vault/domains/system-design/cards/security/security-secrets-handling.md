---
id: security-secrets-handling
node: security.authz
type: qa
---
## Q
Where do service credentials (DB passwords, API keys) live in a well-designed 2026 system, and what beats static secrets entirely?

## A
- Never in code, images, or plain env files — those leak via repos, logs, and crash dumps.
- **Secret manager** (Vault, AWS/GCP Secrets Manager): centralized storage, access audit, automatic **rotation**; apps fetch at startup or lease dynamically.
- Better: **eliminate static secrets** — workload identity (IAM roles, SPIFFE, OIDC federation between platforms) issues short-lived credentials based on *what the workload is*, so there is nothing long-lived to steal or rotate.

Service-to-service trust inside the mesh: **mTLS**, so both ends authenticate with certificates and traffic is encrypted everywhere, not just at the edge.

## Q zh
在设计良好的 2026 系统中，服务凭证（DB 密码、API key）活在哪里，什么完全打败静态秘密？

## A zh
- 绝不在代码、镜像或纯 env 文件 — 那些通过仓库、日志和崩溃转储泄漏。
- **秘密管理器**（Vault、AWS/GCP Secrets Manager）：集中存储、访问审计、自动**轮换**；应用在启动时获取或动态租约。
- 更好：**消除静态秘密** — 工作负载身份（IAM 角色、SPIFFE、平台间 OIDC 联盟）基于*工作负载是什么*发短生命周期凭证，所以无长生命周期来偷或轮换。

网格内服务间信任：**mTLS**，所以两端用证书认证，流量处处加密，不仅边缘。
