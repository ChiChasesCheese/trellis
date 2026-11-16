---
id: ail-evals-leaderboards-choosing-by-a-leaderboard
node: evals.leaderboards
type: qa
step: 3
---
## Q
你们要给客服机器人选模型，同事说"选 Arena 榜首或综合指数最高的就行"。这样选会在哪里出错？

## A
**榜单量的是别人的任务：偏好榜会被风格带偏，综合分平均掉了你的任务，大多数榜还不带价格。**

| 做法 | 出错点 |
|---|---|
| 看 Arena 名次 | 投票人偏爱长而排版漂亮的回答；Arena 因此加了"风格控制"，榜单会在原始和控制两种排序间变动 |
| 看综合指数 | 9 项评测里是办公、编程和科研任务，没有专门的客服项 |
| 只看分不看价 | 同一指数下，最高强度的 Opus 5.5 每任务 10.04 美元，GPT-6.1 Sol 最高强度只差 4 分，每任务 1.27 美元 |

另有结构性偏差：2025 年的研究（Leaderboard Illusion）估计，谷歌和 OpenAI 各拿到 Arena 约 19.2% 和 20.4% 的对战数据，83 个开放权重模型合起来只有约 29.7%；Meta 发布 Llama 4 前私下测了 27 个变体。

**新进展（2026 年 10 月）。** Artificial Analysis 在指数 v5 里按每任务成本列出前十名：从 0.96 美元（GPT-6.1 Terra）到 13.04 美元（Claude Fable 5.1）。

<details class="pt"><summary>想一想：客服场景里，你会拿榜单做什么，不拿它做什么？</summary>用榜单把候选缩到两三个，再用自己的几十条真实对话测。榜单告诉你谁值得试，不能告诉你谁适合你。</details>
