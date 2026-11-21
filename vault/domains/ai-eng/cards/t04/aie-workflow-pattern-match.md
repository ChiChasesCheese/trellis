---
id: aie-workflow-pattern-match
node: t04.workflow-patterns-prompt-chaining-routing-parall
type: qa
step: 2
tags: [考点]
---
## Q
**Workflow patterns · 对号入座**｜考点 · 必会

给下面四个需求各选一种模式，并说明代价：

1. 客服入口：账单问题走账单流程，技术问题走技术流程；
2. 用户问题要同时回答，并且需要检查是否含违规内容；
3. 代码库重构：事先不知道要改哪几个文件；
4. 翻译一首诗：初稿之后要反复润色，直到译评通过。

## A
| 需求 | 模式 | 理由 | 代价 |
|---|---|---|---|
| 1 | **Routing** | 类别明确、可分类 | 多一次分类调用；分类错了整条路径错，要单独评测分类器 |
| 2 | **Parallelization（sectioning）** | 回答与审核互相独立，同时跑 | 多一路调用的成本，延迟不增 |
| 3 | **Orchestrator-workers** | 子任务由输入决定，无法预先写死 | orchestrator 本身可能拆错；调用次数不可预测 |
| 4 | **Evaluator-optimizer** | 有评价标准（译评），迭代有收益 | 每轮多两次调用，要设最大轮数以免循环 |

**共同的原则：** 这些模式都是**用延迟和成本换更好的结果**。先用最简单的单次调用，评测发现不够，再选**对应问题形状**的最小模式，不要为了"架构"而加。

**出处：** Anthropic《Building effective agents》（各模式的 When to use；"only increasing complexity when needed"）
