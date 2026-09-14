---
id: ai-llm-judge-biases
node: ai.evals
type: qa
---
## Q
Why use an LLM as the judge when scoring another LLM's outputs, and which systematic biases must the harness design around?

## A
Why: free-form text has no exact-match oracle, and human labeling doesn't scale to every CI run — a judge model scoring against a **rubric** is the workable middle ground.

Known biases to design around:
- **Position bias**: in pairwise comparisons, favors the first (or last) answer — so **swap order and score both ways**.
- **Verbosity bias**: longer answers score higher regardless of quality.
- **Self-preference**: rates output from its own model family higher — prefer a different-family judge.
- **Style-over-substance**: confident, well-formatted wrong answers beat hesitant right ones — rubrics must anchor on factual criteria.

Ground rule: **calibrate the judge against a human-labeled sample** before trusting it; an unvalidated judge is an unvalidated metric.

## Q zh
为什么用 LLM 作为判官来评分另一个 LLM 的输出，测试框架必须围绕哪些系统偏差设计？

## A zh
为什么：自由格式文本没有精确匹配的真值，人工标注无法扩展到每次 CI 运行 — 根据 **标准** 评分的判官模型是可行的中间道路。

必须围绕设计的已知偏差：
- **位置偏差**：在配对比较中，倾向于第一个（或最后一个）答案 — 所以 **交换顺序并双向评分**。
- **冗长偏差**：更长的答案无论质量如何都评分更高。
- **自我偏好**：对来自其自己的模型家族的输出评分更高 — 偏好不同家族的判官。
- **风格优于实质**：自信、格式精良的错误答案击败犹豫的正确答案 — 标准必须锚定在事实标准上。

基本规则：在信任之前 **根据人工标注的样本校准判官**；未验证的判官是未验证的指标。
