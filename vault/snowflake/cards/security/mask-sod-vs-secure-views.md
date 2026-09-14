---
id: mask-sod-vs-secure-views
node: security.column-masking-policies
type: qa
source: snowflake-docs
---
## Q
同样是限制敏感列访问，为什么脱敏策略（masking policy）比为每类用户建一个安全视图（secure view）更适合做治理？

## A
两个原因。一是可管理性：安全视图要按人群建大量视图，衍生出一堆 BI 看板，数量爆炸；脱敏策略写一次即可挂到跨库跨模式的上千个同类型列。二是职责分离（SoD，segregation of duties）：策略管理员与对象所有者是分开的角色，默认情况下对象所有者既不能解除列上的脱敏策略，也看不到被脱敏的原始数据，甚至 ACCOUNTADMIN 也可被策略阻止查看；安全视图没有这种职责分离。
