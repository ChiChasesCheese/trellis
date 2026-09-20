---
id: problems-pastebin-byte-vs-count-weighted-storage
node: problems.foundations.pastebin
type: cloze
step: 2
tags: [grown]
---
In a pastebin design where pastes split by count into three size tiers (85% snippets averaging 1.5KB, 13% logs averaging 80KB, 2% large files averaging 3MB), the large-file tier — only 2% of pastes by count — accounts for about {{c1::84%}} of total daily bytes written. This shows why {{c2::a single count-weighted average paste size}} badly understates real storage pressure: capacity must be estimated per size tier and summed, not from one blended average.

## zh
在一个按数量分为三档的 pastebin 设计中（85% 片段档均值 1.5KB，13% 日志档均值 80KB，2% 大文件档均值 3MB），仅占数量 2% 的大文件档贡献了当日新增字节量的约 {{c1::84%}}。这说明 {{c2::单一的、按条数加权的平均粘贴大小}} 会严重低估真实的存储压力：必须按大小分档分别估算再求和，而不是用一个笼统的平均值。
