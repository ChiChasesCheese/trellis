---
id: ai-guardrails-validation
node: ai.evals
type: qa
---
## Q
"Guardrails" around an LLM are best understood as which classic backend pattern, and what runs on each side of the model call?

## A
**Validation layers at a trust boundary** — the model is an untrusted component whose input and output both need checking.

- **Input side**: prompt-injection screening (user text and *retrieved documents* are attacker-controlled input), PII redaction, topic/policy filters.
- **Output side**: **schema validation** for structured output (parse-or-retry, the single highest-value guardrail), content/policy classifiers, groundedness checks against sources.

Design rules: run **deterministic checks first** (regex, JSON schema — free) and probabilistic ones (classifier or judge-model calls) after; they add latency, so run them **in parallel with streaming** or accept buffering the response. On failure: retry with the error fed back, fall back, or refuse — never ship unvalidated output downstream.

## Q zh
LLM 周围的"guardrails"最好理解为哪个经典后端模式，模型调用的每一侧运行什么？

## A zh
**信任边界处的验证层** — 模型是一个不受信任的组件，其输入和输出都需要检查。

- **输入侧**：prompt 注入筛选（用户文本和 *检索到的文档* 是攻击者控制的输入），PII 编辑，主题/策略过滤。
- **输出侧**：结构化输出的 **schema 验证**（parse-or-retry，最高价值的单一 guardrail），内容/策略分类器，针对源的 groundedness 检查。

设计规则：首先运行 **确定性检查**（正则表达式、JSON schema — 免费）然后是概率性检查（分类器或判断模型调用）；它们增加延迟，所以 **与流并行运行** 或接受缓冲响应。失败时：用反馈的错误重试，回退，或拒绝 — 永远不要发送未验证的输出到下游。
