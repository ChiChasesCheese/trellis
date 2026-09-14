---
id: ai-eval-set-vs-ab
node: ai.evals
type: qa
---
## Q
For an LLM feature, what plays the role of unit tests vs canary/A-B — and why can't "I tried five prompts and it looked good" replace either?

## A
- **Offline eval set** = the unit/regression suite: a versioned dataset of real inputs with expected outputs or scoring rubrics, run automatically on every prompt/model/pipeline change. Cheap, reproducible, **gates deploy**.
- **Online A/B** = the canary: real traffic, real outcome metrics (task completion, thumbs, escalation rate). Catches distribution drift and UX effects offline sets can't, but is slow, noisy, and burns users on bad variants.

Manual spot-checks fail because outputs are **nondeterministic and high-variance**: five samples can't distinguish a 2% from a 10% failure rate, so eval sets need hundreds of cases and **score thresholds, not exact-match assertions**.

## Q zh
对于 LLM 功能，什么扮演单元测试与金丝雀/A-B 的角色 — 为什么"我试了五个提示词看起来不错"不能替代任何一个？

## A zh
- **离线 eval 集** = 单元/回归测试套件：真实输入的有版本的数据集，带有预期输出或评分标准，在每次 prompt/模型/管道变化时自动运行。廉价，可重复，**控制部署**。
- **在线 A/B** = 金丝雀：真实流量，真实成果指标（任务完成、点赞、升级率）。捕捉离线集无法发现的分布偏移和用户体验效应，但是慢、嘈杂，并且会因为坏变体而伤害用户。

手动抽查失败是因为输出 **不确定且高方差**：五个样本无法区分 2% 和 10% 的失败率，所以 eval 集需要数百个用例和 **评分阈值，而不是精确匹配断言**。
