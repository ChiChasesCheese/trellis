---
id: ail-evals-leaderboards-what-each-measures
node: evals.leaderboards
type: qa
step: 1
---
## Q
新闻里常引用的几个榜单（SWE-bench Pro、Terminal-Bench、ARC-AGI、HLE、Arena、Artificial Analysis 指数）各自在量什么？

## A
**每个榜只量一件事：编程榜量改代码，推理榜量没见过的谜题，知识榜量难题，Arena 量人的偏好，指数把它们加权平均。**

| 榜 | 量什么 | 要小心 |
|---|---|---|
| SWE-bench Pro（Scale） | 真实仓库的 issue，隐藏测试判分；公开 731 题，私有商业集 276 题 | 脚手架不同分就不同 |
| Terminal-Bench | 在命令行里完成任务（指数用 4.0 版） | 版本一换分数不能比 |
| ARC-AGI-3 | 交互小游戏，满分 = 和人一样高效通关 | 只测一类抽象推理 |
| HLE-Diamond | 1,000 道前沿难题，推理与知识各半 | 是问答，不是做事 |
| Arena | 真人匿名对战投票 | 人偏爱长而漂亮的回答 |
| AA 智能指数 v5 | 9 项评测，四类各占 25% | 平均会掩盖单项 |

**新进展（2026 年 3 月）。** ARC-AGI-3 上线，把静态谜题换成需要探索的交互游戏，上线时最好成绩（Gemini 3.1 Pro）还不到 1%。

<details class="pt"><summary>想一想：为什么交互游戏比静态谜题更难靠背题刷分？</summary>每个游戏的规则要在现场探索才能发现，没有现成的题和答案可背，模型必须边试边学，这正是它在没见过的任务上泛化能力的体现。</details>
