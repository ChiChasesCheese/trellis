---
id: infra-flags-deploy-release
node: infra.delivery
type: cloze
---
Feature flags separate {{c1::deploy}} (code reaches production, dark and inert) from {{c2::release}} (behavior exposed to users) — shipping becomes routine and low-stakes, exposure becomes a runtime decision per cohort, and reverting is an instant {{c3::kill switch (flag off)}} instead of a redeploy. The tax: stale flags multiply untested code-path combinations, so every flag needs an owner and an expiry.

## zh
Feature flag 分离 {{c1::deploy}}（代码到达生产，黑暗和惰性）从 {{c2::release}}（行为暴露给用户）——发货变得例行且低赌注，暴露变成每个群体的运行时决定，回滚是即时 {{c3::kill switch（标志关闭）}}而不是重新部署。税：过时标志乘以未测试的代码路径组合，所以每个标志需要一个所有者和过期。
