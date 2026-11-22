---
id: aie-memory-compaction-loss
node: t04.agent-state-memory-session-state-external-store
type: qa
step: 2
tags: [考点]
---
## Q
**Memory · compaction 的信息损失**｜考点 · 必会

对话越来越长，context 快装不下了。方案 A：删掉最早的消息（FIFO）；方案 B：把早期对话压缩成摘要。各有什么风险？

## A
| 方案 | 做法 | 风险 |
|---|---|---|
| **A. FIFO** | 先进先出，最早的消息先移出（常见做法：只保留最近 N 条消息或 N 个 token） | 假设"早期消息不重要"。可能**致命地错**：最早的消息往往说明了**对话的目的** |
| **B. 摘要** | 用同一个或另一个模型总结对话，换掉原文 | 摘要会**丢掉它没觉得重要的细节**，且无法判断丢了什么 |

**更好的做法：**
- 摘要 + **跟踪命名实体**（人名、订单号、日期）；
- 摘要后，把"摘要遗漏的关键信息"补回新的 memory（Bae et al., 2022 用分类器逐句判断保留哪些）；
- 让 agent 在每个动作后**反思**这条新信息要插入、合并，还是替换旧信息（旧信息过时或与新信息矛盾时）（Liu et al., 2023）；
- 关键事实写入外部 store，不依赖摘要。

**遇到矛盾信息：** 有人保留较新的，有人让 AI 判断保留哪个；怎么处理取决于用例。矛盾会让 agent 困惑，也可能帮它看到不同视角。

**实践：** 任务的目标、约束、用户明确提出的要求这类"不可丢的"信息，单独存放，每次都放进 context，不参与摘要。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch6 §Memory（FIFO、summarization、contradiction）

</details>
