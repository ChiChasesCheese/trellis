---
id: aid-four-forms-pick
node: t01.completion-chat-agent-background-async
type: qa
step: 3
tags: [考点]
---
## Q
**选哪种形态**｜考点 · 必会

三件事：(1) 给一个函数补完剩下三行；(2) 把 40 个文件里旧的日志 API 换成新的，每个文件都要跑测试；(3) 周五下班前丢一个"升级某个依赖并修好测试"的任务，周一早上看结果。各选哪种形态？为什么？

## A
| 任务 | 形态 | 理由 |
|---|---|---|
| 补三行 | completion | 上下文就在光标旁，你一眼能判断对错，开 agent 反而慢 |
| 40 个文件换 API | agent（本机或批量脚本） | 要读很多文件、改、跑测试、看结果再继续；有现成的 check 可以自动验证 |
| 周五丢到周一看 | background async | 不占你的机器、不需要你盯着；前提是任务有明确的"做完"判据，且它只能动一个分支 |

**判断顺序：** ① 这件事我一眼能验证吗？能，用 completion/chat；② 需要读多个文件、跑命令吗？是，用 agent；③ 我愿意不看过程只看结果吗？是，且有自动检查，才用 background async。

**常见错法：** 无人值守的任务没有 check，周一看到的是"看起来完成了"的 diff，你得自己当测试套件。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Let Claude run without you：Before a run goes unattended，五个问题）

</details>
