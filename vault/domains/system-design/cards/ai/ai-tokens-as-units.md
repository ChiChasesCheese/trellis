---
id: ai-tokens-as-units
node: ai.foundations
type: qa
---
## Q
LLM pricing, rate limits, and context limits are all denominated in "tokens", not characters or words. What is a token, and what should a backend engineer assume when sizing requests?

## A
A **token** is a chunk of text (~3–4 English characters, ~0.75 words) from a fixed vocabulary the model was trained on; a tokenizer deterministically splits any string into them.

Sizing rules of thumb:
- English prose ≈ **4 chars/token**; code, JSON, other languages, and rare strings (UUIDs, base64) tokenize **much worse** — sometimes 1 token per character.
- Character counts are a bad proxy — count tokens with the model's own tokenizer for quotas and truncation logic.
- Every quota that matters — cost, rate limit, context limit — is input tokens + output tokens.

## Q zh
LLM 定价、速率限制和上下文限制都用"token"表示，而不是字符或单词。什么是 token，后端工程师在调整请求大小时应该假设什么？

## A zh
**Token** 是来自模型训练的固定词汇的文本块（~3–4 英文字符，~0.75 单词）；tokenizer 确定性地将任何字符串分割成它们。

调整大小的经验法则：
- 英文散文 ≈ **4 字符/token**；代码、JSON、其他语言和罕见字符串（UUID、base64）tokenize **糟糕得多** — 有时 1 token 每个字符。
- 字符计数是个坏代理 — 使用模型自己的 tokenizer 计数 token 用于配额和截断逻辑。
- 每个重要的配额 — 成本、速率限制、上下文限制 — 是输入 token + 输出 token。
