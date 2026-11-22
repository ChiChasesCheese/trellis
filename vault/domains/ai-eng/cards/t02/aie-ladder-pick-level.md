---
id: aie-ladder-pick-level
node: t02.simplest-thing-first-workflow-agent
type: qa
step: 2
tags: [考点]
---
## Q
**Simplest thing first · 选哪一级**｜考点 · 必会

下面三个需求，各应该从哪一级开始？说出理由和什么情况下才升级。

1. 把用户留言分成"账单 / 技术 / 其他"三类；
2. 写一篇长文：先出提纲，检查提纲合格后再写正文；
3. 修一个跨多个文件的 bug：要看哪些文件事先不知道，改完要跑测试再改。

## A
| 需求 | 起点 | 理由 | 升级条件 |
|---|---|---|---|
| 1 分类 | **① 单次调用** | 任务单一、输出是几个固定类别 | 评测里准确率不达标，先改 prompt、加示例，仍不够再考虑 |
| 2 提纲再正文 | **② workflow（prompt chaining）** | 步骤固定：提纲 → 检查 → 正文；每步输出作下一步输入 | 检查关卡经常卡住时，再看是否需要循环改写 |
| 3 修 bug | **③ agent** | 要改哪些文件由输入决定，且可以用测试结果作为反馈，反复迭代 | 无需升级；要加停止条件和人工审查 |

**判断口诀：**
- 步骤能事先写下来 → workflow；
- 步数事先不知道、能从环境得到反馈 → agent；
- 其他先用单次调用。

**注意：** 需求 3 能用 agent，是因为**测试结果是可验证的反馈**。没有这种反馈的开放任务，agent 的错误更难发现。

<details class="pt" markdown="1"><summary>出处</summary>

Anthropic《Building effective agents》（Prompt chaining、Agents、Appendix 1: Agents in practice）

</details>
