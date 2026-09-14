---
id: auto-suspend-when-to-disable
node: warehouse.auto-suspend-resume
type: qa
source: snowflake-docs
---
## Q
什么情况下可以考虑关闭虚拟仓库（virtual warehouse）的 auto-suspend（自动挂起）？要付出什么代价，怎么关？

## A
两种情况：仓库承担持续、稳定的重负载；或要求仓库随时可用、完全不能有启动延迟。仓库启动通常很快（约 1–2 秒），但视规格和云上可用资源也可能更久。代价是仓库在没有查询时也持续消耗 credit（信用点），规格越大（X-Large、2X-Large 等）越可观。关闭方法：界面中选 Never，或在 SQL 中把 AUTO_SUSPEND 设为 0 或 NULL。
