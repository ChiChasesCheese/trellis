---
id: cloud-services-coordinates-sign-in-to-dispatch
node: architecture.cloud-services-layer
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 中，一条查询从用户登录到真正开始在计算集群上运行，中间由哪一层负责串联，这一层扮演什么角色？

## A
由云服务（Cloud Services）层串联。它是一组协调性服务的集合，把 Snowflake 的各个组件粘合起来处理用户请求：从登录（sign-in）时的身份认证，到解析、优化查询，再到把查询派发（dispatch）给虚拟仓库（virtual warehouse，计算集群）执行。它是“协调者”而非“执行者”——真正扫描数据的是虚拟仓库。
