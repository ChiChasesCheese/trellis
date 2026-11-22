---
id: aid-ai-bug-hypothesis
node: t05.ai-bug
type: qa
step: 2
tags: [考点]
---
## Q
**定位 bug · 验证它的假设**｜考点 · 追问

agent 说："根因是缓存没有失效，我加了一行清缓存。"测试变绿了。你还要确认什么？

## A
| 问题 | 为什么 |
|---|---|
| 复现测试在**修复之前**是红的吗？ | 否则测试不证明任何事 |
| 去掉修复，测试会不会再红？ | 确认是这一行起了作用，不是巧合 |
| 根因对吗，还是只掩盖了症状？ | 清缓存可能只是让下一次请求绕开了真正的问题（如竞态、过期时间算错） |
| 同类问题还有没有？ | 搜索相同模式的其他调用点 |

**做：** 让 agent 解释"为什么这个改动能解决"并给出**可观察的证据**（日志、断点输出）；你复述核对。
**别做：** 看到变绿就合并。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Give Claude a check to run：ask Claude for evidence）

</details>
