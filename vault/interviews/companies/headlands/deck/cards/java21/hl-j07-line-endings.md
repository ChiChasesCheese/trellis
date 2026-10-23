---
id: hl-j07-line-endings
node: java21.j07-text-blocks
type: qa
step: 7
---
## Q
源文件用 `\n`、`\r\n` 还是 `\r` 换行，对文本块的内容有影响吗？

## A
**没有影响**：文本块里的换行一律规范化为 `\n`，所以 Windows 和 macOS 编辑的结果相同。
