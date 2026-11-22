---
id: aid-license
node: t06.license-copyright
type: qa
step: 1
tags: [摘要]
---
## Q
**License 与 copyright**｜摘要 · 追问

agent 生成的一段代码，和某个开源项目里的函数几乎一样。合规上要担心什么？先做什么？

## A
**三个问题：**

| 问题 | 怎么处理 |
|---|---|
| 生成的代码**像不像**某个受许可证约束的代码 | 对可疑的较长片段做相似度检查；不要把成块的开源代码当"AI 写的"收下 |
| 引入的**依赖**许可证是否兼容 | 许可证扫描进 CI（与是否 AI 引入无关，但 agent 引入依赖更快） |
| 供应商的**条款**怎么说 | 读企业条款：数据是否用于训练、是否有赔偿承诺、**承诺的范围**（哪些产品、哪些条件、是否要求打开过滤） |

**别假设：** 不同计划（消费者、团队、企业）的条款不同；官方文档区分了 Commercial Terms 和 Consumer Terms。赔偿承诺是否存在、覆盖什么，**以你签的合同为准**，不要靠印象。

**做：** 法务审一次供应商条款；工程侧做依赖许可证扫描和相似度检查。
**别做：** 因为"是 AI 写的"就认为没有版权问题，或认为一定有。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Security》（Privacy safeguards：Commercial vs Consumer Terms）

</details>
