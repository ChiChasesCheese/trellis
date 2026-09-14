---
id: reliability-deploy-strategies
node: reliability.resilience.containment
type: qa
---
## Q
Blue-green vs canary vs rolling deployment: what does each optimize for, and which one actually validates a release?

## A
- **Rolling**: replace instances in batches. Cheap (no spare fleet), but old and new run mixed for a while and rollback means rolling again — slowest to undo.
- **Blue-green**: full duplicate fleet, atomic traffic switch. **Fastest rollback** (flip back), no version mixing — but 2x capacity cost, and 100% of users hit a bad release at once.
- **Canary**: route a small slice (1→5→25→100%) to the new version while comparing its SLIs against baseline. The only strategy that **validates with real traffic before full exposure** — requires automated metric analysis to be more than theater.

Modern default: canary for validation, with blue-green-style instant rollback as the escape hatch. All three require [[architecture-schema-compat-rules]]-style compatibility since two versions run concurrently.

## Q zh
Blue-green vs canary vs rolling deployment：每个优化什么，哪个实际验证版本？

## A zh
- **Rolling**：分批替换实例。便宜（无备用舰队），但旧版和新版混合运行一段时间，回滚意味着再次滚动——最慢撤销。
- **Blue-green**：完整重复舰队，原子流量切换。**最快回滚**（翻回），无版本混合——但 2 倍容量成本，100% 用户同时命中坏版本。
- **Canary**：将一个小片段（1→5→25→100%）路由到新版本同时比较其 SLI 与基线。唯一**用真实流量在完全暴露前验证**的策略——需要自动化指标分析不只是舞蹈。

现代默认：用于验证的 canary，带有 blue-green 风格的即时回滚作为逃生舱口。所有三个都需要 [[architecture-schema-compat-rules]] 风格的兼容性，因为两个版本并发运行。
