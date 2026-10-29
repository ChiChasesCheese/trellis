---
id: uth-devtools-editor-buffers-1-gap
node: devtools.editor-buffers
type: qa
step: 1
---
## Q
**Emacs 的缓冲区带一个“空洞”**｜Emacs · 30.1

在文本中间连续打字，为什么不用每次都挪动后面的内容？

## A
**结构。** 间隙缓冲区（gap buffer）：一块连续内存，光标处留一段空白（gap），文本被它分成前后两段。

**细节。**

- 在光标处插入就是写进间隙，O(1)；删除就是让间隙变大
- 光标跳到别处，要把间隙搬过去（`gap_left` 和 `gap_right` 里的内存拷贝），代价与移动距离成正比
- 间隙不够时，`make_gap_larger` 多要 `GAP_BYTES_DFL` = 2000 字节

**为什么。** 编辑集中在光标附近，连续内存比“每行一个对象”或链表更省内存、更利于缓存；只有跳转后的第一次编辑才付搬迁代价。

**对应 LeetCode：** LC 2296 设计一个文本编辑器 · LC 232 用栈实现队列
