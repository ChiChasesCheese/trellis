---
id: cc-round-formats-proctored-ide
node: round.formats
type: qa
---
## Q
The assessment runs in a proctored browser IDE: no debugger, no local files, tab focus is logged and pasted text is flagged and compared across submissions. Name three concrete adaptations.

## A
**Treat the environment as part of the problem.**

- Type from scratch. Pasted solutions are detected and similarity-matched; memorize the *shape* of an idiom, never the text.
- Debug with prints to stderr only — there is no breakpoint, and stdout is the graded channel. See [[cc-round-debug-stderr-only]].
- Keep the tab focused: read the whole statement, and take your notes, inside the IDE rather than switching to a doc — focus loss is logged and reads as looking something up.

## Q zh
笔试跑在受监考的浏览器 IDE 里：没有 debugger、没有本地文件，切换标签页会被记录，粘贴的文本会被标记并跨提交做相似度比对。说出三条具体的适应做法。

## A zh
**把环境本身当作题目的一部分。**

- 从零手打。粘贴的答案会被检测并做相似度匹配；记住写法的**形状**，绝不背文本。
- 只用打到 stderr 的 print 来调试 —— 没有断点，而 stdout 是被评分的通道。见 [[cc-round-debug-stderr-only]]。
- 保持标签页聚焦：在 IDE 内读完整题面并记笔记，而不是切到文档 —— 失焦会被记录，看起来像在查资料。
