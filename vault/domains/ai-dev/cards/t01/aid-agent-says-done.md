---
id: aid-agent-says-done
node: t01.coding-agent-loop-tools-context
type: qa
step: 2
tags: [考点]
---
## Q
**"我做完了"可信吗**｜考点 · 必会

agent 的总结写着"所有测试通过"。你该怎么确认？这句话在 loop 里处于什么位置？

## A
**位置：** 这句话是模型**生成的文本**，不是 tool 的返回结果。只有 tool 返回（测试的真实输出、退出码）才是环境给的"地面真相"。

**做：** 让它给**证据**——跑过的命令和输出，或截图；看 exit code，不看形容词。
**别做：** 只读总结就合并。官方文档的说法是：agent 在"看起来做完"时停下；如果没有可运行的检查，"看起来完成"就是它仅有的依据。

| 总结里的句子 | 你要看的 |
|---|---|
| "所有测试通过" | 命令、输出、退出码 |
| "已修复登录 bug" | 能复现的失败测试变绿 |
| "页面已更新" | 截图或实际请求的响应 |

**追问：** 如果它没有任何可运行的检查呢？那就先给它一个（见 t02 的 check 一叶），再让它动手。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Give Claude a check to run：ask Claude for evidence）

</details>
