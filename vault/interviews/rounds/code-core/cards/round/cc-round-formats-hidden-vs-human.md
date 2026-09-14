---
id: cc-round-formats-hidden-vs-human
node: round.formats
type: qa
---
## Q
You are handed the same problem twice: once as a 60-minute timed assessment graded by ~20 hidden tests, once as a live phone screen with an engineer watching. Name what changes about how you spend the hour.

## A
**The grader changes, so the artifact changes.** Hidden tests score only the bytes your program writes for inputs you never see; a person scores the reasoning, the naming, and how you recover from a mistake.

- Timed OA: buy correctness on boundary cases, not elegance. A comment earns nothing; spelling the empty-result sentinel right earns a test.
- Live screen: say the trade-off before you type it, keep names legible, ask before you assume — the transcript is the deliverable.
- Both: a part that runs beats a part that is beautifully half-written.

## Q zh
同一道题给你两次：一次是 60 分钟、由约 20 个隐藏测试评分的限时笔试，一次是有工程师在线观看的电话面试。说出这一小时的花法有什么不同。

## A zh
**评分者变了，交付物就变了。** 隐藏测试只看你的程序对没见过的输入写出的字节；活人看的是推理、命名，以及你如何从错误中恢复。

- 限时 OA：把时间买在边界正确性上，而不是优雅。注释不得分；把空结果的 sentinel 拼对就能拿一个测试。
- 现场面试：在敲代码之前先说清取舍，名字要可读，假设之前先问 —— 对话记录才是交付物。
- 两者共通：能跑的一部分胜过写得很漂亮的半部分。
