---
id: tc-design-review-dialogue
node: t05.design-review-dialogue
type: qa
step: 1
tags: [惯用说法]
---
## Q
**Design review dialogue · 评审里的对话**｜惯用说法 · 必会

你在 design review 里被问到："Why not just use a managed service?" 你有理由，但也承认对方的点有道理。怎么回答，既不防御又不丢掉立场？

## A
**可以这么说：**
- "That's a fair question. We looked at it, and the main blocker was data residency."
- "Good point. I hadn't weighed the on-call cost; let me add that to the doc."
- "I see the appeal. The trade-off for us is less control over upgrades."
- "I don't have the numbers on hand. I can follow up after the review."
- "Let me make sure I understand your concern: you're worried about vendor lock-in, right?"

**别这么说：**
- "That's not a problem." （没回答问题，听起来在驳回对方）
- "We already decided that." （关上了讨论的门）

**语气：** 先承认问题合理，再给理由或承认缺口。被问到不会的，直接说不知道并承诺补上，比硬撑更可信。

**评审里的角色：** 作者要说明范围、备选和代价；评审者提出的是"问题和风险"，不是对作者的评价。回复时把"你"换成"这个方案"。

<details class="pt" markdown="1"><summary>出处</summary>

惯用说法，非引用；评审流程参考 Orosz《The Software Engineer's Guidebook》ch15 §1 Design Documents, RFCs and Architecture Documents

</details>
