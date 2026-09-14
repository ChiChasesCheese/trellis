---
id: netpol-internal-stage-parameter
node: security.network-policies-private-connectivity
type: qa
source: snowflake-docs
---
## Q
AWS 上的 Snowflake 账户已经配好 `MODE=INGRESS` 的 IPv4 网络规则，但内部 stage（internal stage，Snowflake 托管的文件暂存区）依然能从任意 IP 访问。可能漏了什么？还有哪些情况规则保护不到 stage？

## A
账户管理员必须先开启 `ENFORCE_NETWORK_RULES_FOR_INTERNAL_STAGES` 参数，否则无论规则的 mode 是什么，网络规则都不保护内部 stage。开启后，一条 IPv4 + INGRESS 规则可同时保护服务和内部 stage。仍保护不到的情况：IPv6 规则只保护服务、不保护 stage；挂在安全集成上的网络策略不限制 stage 访问；Azure 上不能用网络规则限制内部 stage（只能借助 Azure Private Link 阻断公网访问）。
