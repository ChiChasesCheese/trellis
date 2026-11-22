---
id: aid-context-clear-habits
node: t01.context-window
type: qa
step: 2
tags: [实践]
---
## Q
**Context window · 清理与压缩的时机**｜实践 · 必会

同一个 session 里你先修了 bug，又让它写文档，现在想开始第三件完全无关的事。该怎么做？

## A
**做：** 任务之间 `/clear`（Claude Code 的命令，清空对话重新开始）；必须延续时用 `/compact <重点>`，例如"保留 API 改动和测试命令"。
**别做：** 把三件无关的事塞进同一个 session。每次请求都会重发前两件的历史；缓存热的时候有折扣，过期后全价。

| 场景 | 动作 |
|---|---|
| 换一个无关任务 | `/clear` |
| 同一任务，历史太长但还要继续 | `/compact` 加上要保留的重点 |
| 同一错误纠正两次仍不对 | `/clear`，把学到的写进一条新提示（见 t02 纠偏） |
| 一个大文件或输出撑爆 context | 别让它整个读；让它搜索或只读片段 |

**时效标注（2026-11 官方文档）：** 多数现行模型的窗口是 1M token，且会自动 compaction，"撑爆"已不常见；但官方仍建议任务间 `/clear`，因为聚焦的 context 答得更好，也更便宜。窗口大小会随模型变，"越满越差、无关内容有成本"这个机制不变。

**出处：** Claude Code docs《Best practices》（Keep cost and context down；What you can stop doing）
