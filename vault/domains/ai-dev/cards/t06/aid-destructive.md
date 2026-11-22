---
id: aid-destructive
node: t06.destructive-operations
type: qa
step: 1
tags: [实践]
---
## Q
**Destructive operations 的防护**｜实践 · 必会

agent 在清理"无用分支"时执行了 `git push --force` 并删除了远程分支。怎么设计，让这种事不可能发生，而不只是"希望它不会"？

## A
**四层防线：**

| 层 | 做法 | 性质 |
|---|---|---|
| **最小权限** | agent 只有它这次任务需要的凭据；没有生产写权限、没有删库权限 | 确定性 |
| **备份** | 数据库、对象存储有可恢复的备份；定期演练恢复 | 事后 |
| **人工确认点** | 强推、删分支、生产部署：`ask` 规则或 hook，必须人批准 | 确定性 |
| **服务端保护** | 分支保护规则、禁止强推；agent 的凭据无法绕过 | 确定性 |

**官方的几个事实（2026-11）：**
- auto mode 默认会拦下"生产部署""强推覆盖他人工作"这类动作，但它是分类器，不是保证；
- 云端 session 里，GitHub 代理会拒绝删除分支和推送非分支（如 tag）；
- 无人值守的定时任务，先在 `main` 上设一条该任务**绕不过**的分支规则。

**别做：** 把"不要强推"写进 CLAUDE.md 当唯一防线。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Let Claude run without you；Start runs on a schedule）；《Security》（Cloud execution security：Push restrictions）

</details>
