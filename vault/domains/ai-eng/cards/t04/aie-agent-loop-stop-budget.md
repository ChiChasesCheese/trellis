---
id: aie-agent-loop-stop-budget
node: t04.agent-loop-stop-condition-max-steps-budget
type: qa
step: 2
tags: [实践]
---
## Q
**Agent loop · stop condition、max steps、budget**｜实践 · 必会

一个调研 agent 上线后，有一次对同一个搜索接口反复调用，一夜烧掉很多费用。该给 agent loop 加哪些"刹车"？怎么知道它是不是在做无用功？

## A
**原则：** 没有终止条件的循环会一直转。每个循环都要有**明确的出口**，由代码强制，而不是靠模型自觉。

| 刹车 | 做法 | 触发后 |
|---|---|---|
| **Max steps** | 限制迭代次数（Anthropic 建议的 stopping condition） | 停止，把已有结果和未完成项交给人 |
| **Budget** | 每个任务的 token / 费用 / 时间上限 | 停止并告警 |
| **Done 判断** | 完成必须有**可检查的依据**（如测试通过），不能只靠模型说"我做完了" | 不满足就不算完成 |
| **重复检测** | 连续相同的 tool 调用 + 相同参数，视为卡住 | 换策略或停止 |

**为什么 done 判断不能信模型：** 书里的反例：让 agent 把 50 个人分到 30 个房间，它只分了 40 个，却坚持说任务完成了，这叫 reflection 出错。

**怎么知道是不是无用功（效率指标）：**
- 完成一个任务平均要多少步？
- 平均花多少钱？
- 每种动作平均多久？有没有特别慢或贵的？
- 与基线（另一个 agent 或人工）比较；注意 AI 与人的效率标准不同：同时访问 100 个网页对人低效，对 AI 很简单。

**别忘了时间也是约束：** 比如写标书的 agent，过了截止时间才交，就没有价值。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch6 §Agent Failure Modes and Evaluation（Planning failures、Efficiency）；Anthropic《Building effective agents》（stopping conditions，如 maximum iterations）

</details>
