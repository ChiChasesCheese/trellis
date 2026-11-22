---
id: aie-agent-evals-outcome-passk
node: t05.agent-evals-trajectory-tool-calls-end-state-chec
type: qa
step: 1
tags: [摘要]
---
## Q
**Agent evals · 评结果还是评过程**｜摘要 · 必会

订票 agent 对用户说「已订好」，但数据库里没有订单。评测应该看它说了什么，还是看数据库？还有，同一任务跑 3 次、每次 75% 成功，用户体验到的可靠性是多少？

## A
**两种对象：**

| 对象 | 含义 | 例子 |
|---|---|---|
| **transcript**（也叫 trajectory、trace） | 一次尝试的完整记录：输出、tool calls、中间结果 | 看调用了哪些工具、顺序是否合理 |
| **outcome**（end-state check） | 环境的最终状态 | 数据库里是否真有这张订单 |

**优先评 outcome：** 评 agent 产出了什么，而不是走了哪条路。硬性规定步骤顺序会惩罚合理的另一种做法。transcript 用来评过程质量：工具选择、有没有绕远路、无效调用占比、步数和成本。

**grader 的三类：**
- code-based：字符串匹配、单元测试、查数据库状态，快、便宜、可复现，但对合理变体脆弱；
- model-based（LLM-as-judge）：灵活，但不确定、更贵，要对照人工校准；
- human：金标准，贵且慢。

**pass@k 与 pass^k：**
- **pass@k：** k 次尝试里至少成功 1 次的概率，一次成功就算数（如生成代码，多生成几个选能过测试的）；
- **pass^k：** k 次**全部**成功的概率，衡量一致性（面向客户的 agent）。

**回到题目：** 每次成功 75%，3 次全对的概率是 0.75³ ≈ 42%；k = 10 时，pass@k 趋近 100%，pass^k 趋近 0。所以面向客户的 agent 要看 pass^k。

**环境要隔离：** 每次试验从干净环境开始，不留上一次的状态；有状态环境、多轮对话也要这样设计。

<details class="pt" markdown="1"><summary>出处</summary>

Anthropic《Demystifying evals for AI agents》anthropic.com/engineering/demystifying-evals-for-ai-agents（2026-11-21 读）；Huyen《AI Engineering》ch3 §Functional Correctness（pass@k）；ch6 §Agent Failure Modes and Evaluation

</details>
