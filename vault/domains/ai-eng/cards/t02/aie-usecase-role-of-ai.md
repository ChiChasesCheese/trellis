---
id: aie-usecase-role-of-ai
node: t02.use-case-evaluation-llm
type: qa
step: 1
tags: [考点]
---
## Q
**Use case evaluation · AI 在产品里的角色**｜考点 · 必会

产品经理给了两个想法：A）在邮件客户端里，用户一打开邮件就自动弹出 AI 摘要；B）客服后台里，AI 给人工客服推荐三条回复草稿。哪一个对质量要求更高？为什么？上线后怎么逐步提高自动化程度？

## A
**看三个维度：**

| 维度 | 含义 | 对要求的影响 |
|---|---|---|
| Critical / complementary | 没有 AI，产品还能不能用 | AI 越关键，要求越高；不关键时用户更能容忍错误 |
| Reactive / proactive | 用户提出请求才响应，还是在合适的时机主动弹出 | **主动**的功能用户没要求过，质量低就像骚扰，所以质量门槛更高；被动功能一般要求快 |
| Dynamic / static | 随用户反馈持续更新，还是周期更新 | 动态的要有持续的更新机制 |

**回到题目：** A 是主动弹出的，用户没请求，摘要出错会被当成打扰，**要求更高**。B 的草稿由人工客服把关（human-in-the-loop，让人参与决策），容错高得多。

**逐步放权（Microsoft 的 Crawl-Walk-Run）：**
1. Crawl：必须有人参与；
2. Walk：AI 可以直接和内部员工交互；
3. Run：更高自动化，可以直接面对外部用户。

**例：** 先让 AI 给人工客服推荐回复。如果简单问题的 AI 回复里 95% 被客服原样采用，就可以让客户直接和 AI 对话处理这类简单问题。

**出处：** Huyen《AI Engineering》ch1 §Use Case Evaluation → The role of AI and humans in the application
