---
id: netpol-precedence-specific-wins
node: security.network-policies-private-connectivity
type: qa
source: snowflake-docs
---
## Q
网络策略（network policy）可以分别挂在账户（account）、用户（user）和安全集成（security integration）上。三处都挂了策略时，哪个生效？

## A
最具体的策略覆盖较通用的策略：安全集成级 > 用户级 > 账户级。账户级最通用，会被用户级或安全集成级覆盖；用户级覆盖账户级，但被安全集成级覆盖。因此推荐尽量把策略收窄到一组用户或某个安全集成，而不是整个账户。另外策略创建后必须激活（关联到账户、用户或集成）才开始限制流量。
