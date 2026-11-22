---
id: aid-legacy-map
node: t03.legacy-codebase-architecture-map-glossary-domain
type: qa
step: 1
tags: [实践]
---
## Q
**Legacy codebase · 先建地图**｜实践 · 追问

接手一个 10 年的单体，没有文档。你怎么让 agent 在这里面干活而不是到处乱撞？

## A
| 步骤 | 做法 |
|---|---|
| 1. 只读探索 | 让 agent 读入口、模块依赖、测试布局，**不改任何东西**，产出 architecture map |
| 2. 你校正 | 它的地图只是它读代码后的猜测；错的地方你改（哪个模块其实已死、哪个边界是假的） |
| 3. 存成文件 | 放进仓库（如 `docs/architecture.md`），在 CLAUDE.md 里一行指过去 |
| 4. glossary | 业务词汇对应到代码里的名字（"settlement"＝哪个类） |
| 5. conventions | 记**为什么**："不要直接写库，要走 repository，因为审计日志在那里" |

**记"为什么"而不是"是什么"：** "是什么"读代码就知道；"为什么"（历史决定、坑、被放弃的方案）代码里没有，也正是 agent 会踩的地方。

**官方的例子：** 值得写下的是：到处都是、但新代码不许学的老模式；看起来没用其实有用的目录；团队定的决定。

**别做：** 让 agent 自动生成一整套文档就当真——没人校正过的猜测会固化成"事实"。

**出处：** Claude Code docs《Best practices》（Keep CLAUDE.md short：places where the code is misleading；decisions that aren't in the repo）
