---
id: architecture-api-versioning-strategies
node: architecture.discovery
type: qa
---
## Q
URI versioning (/v2/) vs header versioning vs "no versions, additive-only": when is each the right API evolution strategy?

## A
- **Additive-only evolution** (no version bumps): the modern default — only compatible changes ([[architecture-schema-compat-rules]]), clients ignore unknown fields, breaking changes handled by expand-contract ([[architecture-expand-contract]]). Cheapest: one live version to operate.
- **URI versioning** (`/v2/`): for rare, genuinely breaking redesigns with external consumers — explicit, cacheable, easy to route/deprecate per version. Cost: you now run and support N versions, and internal models fork.
- **Header/date versioning** (e.g. Stripe's pinned API dates): many small versions with server-side translation layers down to one internal model — great DX, but the translation-chain machinery is expensive to build.

Anti-pattern: reflexively minting `/v2/` for changes that could have been additive.

## Q zh
URI 版本化（/v2/）vs header 版本化 vs"无版本，仅可加成"：什么时候每一个是正确的 API 演进策略？

## A zh
- **仅可加成演进**（无版本颠簸）：现代默认——仅兼容改变（[[architecture-schema-compat-rules]]），客户端忽略未知字段，突破改变由扩展-契约处理（[[architecture-expand-contract]]）。最便宜：一个实时版本操作。
- **URI 版本化**（`/v2/`）：对于少见的、真实破坏重设计外部消费者——显式、可缓存、易于路由/弃用每个版本。代价：你现在运行支持 N 版本，内部模型分叉。
- **Header/日期版本化**（例如 Stripe 的固定 API 日期）：许多小版本带服务器端翻译层向下到一个内部模型——很棒 DX，但翻译链机器昂贵构建。

反模式：自反性铸造`/v2/`对可能是可加成的改变。
