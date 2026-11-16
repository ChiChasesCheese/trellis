---
id: ail-models-reasoning-budget-to-effort
node: models.reasoning
type: qa
step: 2
---
## Q
怎么控制模型想多久？思考预算（budget_tokens）和 effort 档位有什么区别，各有什么限制？

## A
**老做法是给一个思考 token 预算；新做法是让模型自己决定想不想、想多深，开发者只调 effort 档位。**

| | 固定预算 | 自适应思考 |
|---|---|---|
| 写法 | `budget_tokens: 10000` | `thinking: adaptive` 加 `effort` |
| 规则 | 至少 1,024，且小于 max_tokens | 档位 low、medium、high、xhigh、max |
| 简单问题 | 照样想 | 低档位可以完全不想 |

```json
{
  "model": "claude-opus-5-5",
  "max_tokens": 16000,
  "thinking": {"type": "adaptive"},
  "output_config": {"effort": "medium"}
}
```

- **默认档位：** Opus 5.5 和 Haiku 5.5 是 medium，多数其他模型是 high。
- **计费：** 思考按输出价全额计费；响应里只给摘要，账单按完整思考算，可查 `thinking_tokens`。
- **max_tokens 是硬上限：** 思考加回答共用它；回答被截断（stop_reason 为 max_tokens）时，要么加大它，要么降低 effort。
- **缓存：** 请求顶层的 effort 或思考配置变了，提示缓存（保存长前缀已算好的 KV 状态以便复用）可能失效，所以一个对话里尽量不改；较新的模型支持按消息改 effort，不破坏缓存。

**新进展（2026 年 2 月 – 11 月）。** Anthropic 从 Claude 4.6 起弃用固定预算，4.7 及之后的模型收到 `budget_tokens` 会直接返回 400 错误，只留自适应思考加 effort。智能体循环里，用户新输入后的第一次请求承担大部分思考，只处理工具结果的后续请求常常可以不想。

<details class="pt"><summary>想一想：一个已缓存的长对话，为了省钱把后面几轮的 effort 从 medium 调成 low，账单会怎样？</summary>顶层的 effort 变了，缓存前缀可能失效，整段长前缀要按新输入重新写入缓存，这一轮可能比不调还贵。想少想一点，应在对话开头就定好档位，或用不破坏缓存的按消息调整方式。</details>
