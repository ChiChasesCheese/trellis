---
id: serverless-qas-billing
node: cost.serverless-feature-billing
type: qa
source: snowflake-docs
---
## Q
仓库开启查询加速服务（Query Acceleration Service, QAS）后，加速部分的费用算在仓库的信用点里吗？同时有 10 条查询在用 QAS 会不会让计费翻 10 倍？

## A
不算在仓库里。QAS 使用无服务器计算，只在服务被使用时按秒计费，并与仓库用量分开计费。费用上限由扩展系数（scale factor）乘以仓库规模决定，与同时使用 QAS 的查询数量无关，所以不会因为并发查询变多而成倍增加。每计算小时消耗的信用点按服务消耗表中的无服务器费率计。
