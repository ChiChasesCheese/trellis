---
id: ai-temperature-sampling
node: ai.foundations
type: qa
---
## Q
What does the `temperature` parameter actually control on an LLM request, and when do you set it low vs high?

## A
The model outputs a **probability distribution over next tokens**; the sampler picks one. Temperature reshapes that distribution: **0 ≈ always pick the most likely token** (near-deterministic — not guaranteed identical across runs), **higher values flatten it** so unlikely tokens get picked more, giving variety and more derailments. `top_p` is a sibling knob that cuts off the improbable tail.

- **Low (0–0.3)**: extraction, classification, code, tool calls, evals — anything you validate or compare.
- **Higher (0.7–1)**: brainstorming, creative drafts, generating diverse candidates.

It is a dial on the **sampler**, not the model — no request-time setting makes the model "know" more.

## Q zh
LLM 请求上的 `temperature` 参数实际上控制什么，何时设置低 vs 高？

## A zh
模型输出 **下一个 token 上的概率分布**；采样器选择一个。温度重塑该分布：**0 ≈ 总是选择最可能的 token**（接近确定性 — 不保证在运行中相同），**更高的值展平它** 所以不太可能的 token 被选择更多，给出多样性和更多脱轨。`top_p` 是一个兄弟旋钮，切断不太可能的尾部。

- **低（0–0.3）**：提取、分类、代码、工具调用、eval — 任何你验证或比较的。
- **更高（0.7–1）**：头脑风暴、创意草稿、生成多样候选。

它是 **采样器** 上的旋钮，而不是模型 — 没有请求时间设置使模型"知道"更多。
