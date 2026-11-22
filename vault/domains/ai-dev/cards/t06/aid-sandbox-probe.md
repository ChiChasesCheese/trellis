---
id: aid-sandbox-probe
node: t06.permission-model-sandbox
type: qa
step: 2
tags: [考点]
---
## Q
**"跳过所有确认"的风险边界**｜考点 · 必会

两种场景：(A) 你在笔记本上，对着生产凭据所在的目录，打开跳过确认；(B) 在一次性容器里，没有凭据、网络只通包仓库，跑一个批量迁移。各自可以接受吗？

## A
**风险 = agent 能做的事 × 被骗或出错的概率。** 去掉确认，是把"人拦一道"换成"只靠环境限制"。

| 场景 | 环境能阻止什么 | 判断 |
|---|---|---|
| (A) 本机、有凭据、通网 | 几乎什么都不能 | **不可接受**：一次 injection 就能读凭据并外发 |
| (B) 一次性容器、无凭据、网络受限 | 凭据读不到、数据发不出、坏了就丢 | **可以接受**：最坏结果有限 |

**做：** 想少点确认，先**缩小爆炸半径**：容器或 VM、最小权限、网络白名单、专用分支；再放宽确认。官方也建议用 dev container 或沙箱运行时包住整个进程。

**别做：** 为了省按键，在带密钥的真实环境里开最宽松的模式。

**出处：** Claude Code docs《Security》（Security best practices：Working with sensitive code）；《Best practices》（Let Claude run without you：它能碰什么）
