---
id: ail-use-context-window-sizes-and-price-tiers
node: use.context-window
type: qa
step: 2
---
## Q
现在主流模型的上下文窗口有多大？一百万 token 大约是多少文字？窗口和输出上限是一回事吗？

## A
**截至 2026 年 11 月，主流旗舰的窗口约 100 万 token（1M），单次最多输出约 12.8 万 token；窗口装的是"输入 + 输出"，输出上限是另一个更小的数。**

| 模型 | 窗口 | 单次输出上限 |
|---|---|---|
| Claude Fable 5.2、Opus 5.5、Sonnet 5.5、Haiku 5.5 | 1M | 128K |
| OpenAI GPT-6 系列（Astra、Sol、Terra、Luna） | 1.05M | 128K |
| 上一代 Claude Opus 4.5、Haiku 4.5 | 200K | 64K |

- **换算：** 1M token 约 55 万个英文词，或约 250 万个字符（Claude 现行分词器）；200K 约 15 万个英文词。
- **输入 + max_tokens 超窗口：** 请求仍被接受，生成到窗口尽头就停（stop_reason 为 model_context_window_exceeded）。

**新进展（2026 年 9 月）。** Opus 5.5、Sonnet 5.5 把整个 1M 窗口按同一个单价计费；而 Haiku 5.5 的提示超过 10 万 token 后单价升到 5 倍，OpenAI 的 GPT-6.1 Sol 超过 27.2 万输入 token 后输入价翻倍。窗口大不等于整个窗口都便宜。

<details class="pt"><summary>想一想：同样一个 80 万 token 的请求，在 Sonnet 5.5 和 GPT-6.1 Sol 上，每百万输入 token 的单价各是多少？</summary>Sonnet 5.5 整个窗口都是每百万 2 美元；GPT-6.1 Sol 超过 27.2 万 token 的请求按长上下文价，每百万 4 美元（输出价也从 10 美元升到 15 美元）。</details>
