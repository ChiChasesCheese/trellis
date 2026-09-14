---
id: ai-grounding-citations
node: ai.rag
type: qa
---
## Q
What does "grounding" mean in a RAG system, and what do enforced citations buy you beyond user trust?

## A
**Grounding**: the answer must be supported by the retrieved passages — the prompt instructs the model to answer *only* from provided context and to **abstain** when the context doesn't contain the answer (the abstain path is what kills hallucinated answers on retrieval misses).

Citations (chunk/source IDs attached to claims) buy:
- **Verifiability**: users and reviewers can check the source.
- **Automated eval**: a groundedness checker can verify each claim is entailed by its cited chunk, and gate deploys on it.
- **Debuggability**: a wrong answer becomes attributable — bad chunk retrieved vs model ignoring a good chunk.

Caveat: models can cite plausibly but wrongly, so citation presence is not proof — verification is a separate check.

## Q zh
在 RAG 系统中"grounding"是什么意思，强制引用除了用户信任还能为你买到什么？

## A zh
**Grounding**：答案必须得到检索的段落的支持 — prompt 指示模型 *仅从* 提供的上下文回答，当上下文不包含答案时 **弃权**（弃权路径是在检索失败时杀死幻觉答案的原因）。

引用（附加到声明的块/源 ID）买入：
- **可验证性**：用户和审阅者可以检查源。
- **自动 eval**：groundedness 检查器可以验证每个声明都由其引用的块蕴含，并在其上控制部署。
- **可调试性**：错误答案变得可归因 — 检索到的块不好 vs 模型忽视了好块。

警告：模型可以合理地但错误地引用，所以引用的存在不是证明 — 验证是一个单独的检查。
