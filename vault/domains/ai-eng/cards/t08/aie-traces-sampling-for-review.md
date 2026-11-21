---
id: aie-traces-sampling-for-review
node: t08.production-traces-eval-set
type: qa
step: 2
tags: [考点]
---
## Q
**Production traces · 每天只能看 50 条，看哪些**｜考点 · 必会

线上每天 5 万条对话，你只有时间看 50 条。纯随机抽 50 条，会漏掉什么？怎么抽更有价值？

## A
**纯随机的问题：** 失败只占小部分（假设 2%）时，随机的 50 条平均只有约 1 条失败，学不到什么；稀有但严重的失败几乎抽不到。

**分层抽样：**

| 层 | 抽法 | 目的 |
|---|---|---|
| 随机 | 少量纯随机 | 估计总体情况、发现没想到的问题 |
| 负面信号 | 差评、立即重新生成、用户说"不对"、中途停止、转人工 | 失败密度高 |
| 自动评分低 | judge 或检查给低分的 | 复核打分 |
| 异常 | 特别长、特别慢、token 特别多、触发 guardrail 的 | 边界情况、攻击 |
| 新模式 | 新版本发布后的前几批、新类型的查询 | 发现回归和漂移 |

**书里提到的信号（可用来分层）：** 用户中途停止生成、重新生成、纠错（"不，我的意思是……"）、投诉、对话轮数、拒答率。

**怎么看：** 直到"不再学到新东西"为止（Hamel）；每条都归到某个 failure mode，数量多的类别先做成评测。

**抽样不等于统计：** 按负面信号抽出的样本不能用来估计总体质量，只用来找问题；估总体用随机那一层。

**出处：** Huyen《AI Engineering》ch10 §Extracting Conversational Feedback（各信号）、§Metrics；Hamel Husain《Your AI Product Needs Evals》（look at data until you stop learning）。2% 与 50 条为示例数字
