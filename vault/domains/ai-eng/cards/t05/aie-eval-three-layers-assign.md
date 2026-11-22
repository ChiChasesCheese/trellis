---
id: aie-eval-three-layers-assign
node: t05.eval-assertion-human-model-review-online-a-b
type: qa
step: 2
tags: [考点]
---
## Q
**Eval 三层 · 该放哪一层**｜考点 · 必会

把下面五个检查分别放到 L1、L2、L3，并说明理由：

1. 回复必须是合法 JSON，且含 `answer` 字段；
2. 回复里不能出现内部系统名称（有一份黑名单）；
3. 摘要是否忠实于原文；
4. 回复语气是否礼貌专业；
5. 新版 prompt 是否让用户的问题解决率上升。

## A
| 检查 | 层 | 理由 |
|---|---|---|
| 1 JSON 与字段 | **L1** | 代码能完全判定，快而便宜，每次改动都跑 |
| 2 黑名单 | **L1** | 字符串匹配 |
| 3 摘要忠实 | **L2** | 需要理解语义；用 LLM judge（要有评分标准），再抽样请人核对 |
| 4 语气 | **L2** | 主观，需要 judge 或人 |
| 5 解决率 | **L3** | 要看真实用户的业务指标，需要线上 A/B |

**原则：** **能用代码判定的，不要用模型判。** 代码判定便宜、稳定、可复现，放在最底层，每次都跑；模型和人的判断留给代码判不了的部分；线上实验留给重大改动。

**常见错误：**
- 把所有检查都交给 judge：贵、慢、不稳定；
- 只做 L1：格式都对，回答不好；
- 太早做 L3：成本高，而 L1/L2 还没把明显的问题清完。

<details class="pt" markdown="1"><summary>出处</summary>

Hamel Husain《Your AI Product Needs Evals》（三层）；Huyen《AI Engineering》ch3 §Exact Evaluation、§AI as a Judge

</details>
