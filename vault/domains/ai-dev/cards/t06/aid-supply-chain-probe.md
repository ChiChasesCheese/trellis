---
id: aid-supply-chain-probe
node: t06.supply-chain-hallucinated-packages-malicious-pac
type: qa
step: 2
tags: [考点]
---
## Q
**Supply chain · 装第三方 skill（按需加载的流程说明）之前**｜考点 · 追问

同事分享了一个"自动化发布"的开源 skill，一行命令就能装进你的 agent。装之前你要查什么？

## A
**skill 不是被动文档，是会被 agent 当指令执行的文字（甚至带脚本）。**

| 检查 | 看什么 |
|---|---|
| 读全文 | SKILL.md 里有没有"忽略之前的规则""把某文件发送到某地址"之类的话 |
| 带的脚本 | 它会执行什么命令；有没有网络请求 |
| 权限 | 它要求的工具范围是否超出任务需要 |
| 来源 | 作者是谁、仓库活跃度、有没有人审过 |
| 版本 | 固定到具体提交，别跟着 `main` 自动更新 |

**做：** 内部审过的 skill 放进团队仓库，大家从那里装；对外部的当作"一段要运行的代码"来审。
**别做：** 因为"只是一个 markdown 文件"就不看。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Put team procedures）；《Security》（Best practices for working with untrusted content）

</details>
