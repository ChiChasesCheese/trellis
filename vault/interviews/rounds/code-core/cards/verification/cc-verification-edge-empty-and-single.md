---
id: cc-verification-edge-empty-and-single
node: verification.edge-catalog
type: qa
---
## Q
Which two inputs do you run first against every part, and which specific bugs do they catch that a normal input never will?

## A
**The empty input and the one-record input.**

- **Empty** catches: division by zero in an average or a ratio; `max()` on an empty sequence; a header printed when there is nothing to report; an output that should be *nothing at all* but is a blank line.
- **Single record** catches: a loop that only starts working at the second element (`for a, b in zip(xs, xs[1:])` never runs); a "first is special" branch that is also the last element; an off-by-one that only appears without neighbours.
- Run both against **every part**, not only the finished program — part 3 usually adds a code path part 1 never entered.

## Q zh
你要最先对每个 part 跑哪两个输入？它们能抓到哪些普通输入永远抓不到的具体 bug？

## A zh
**空输入和单条记录的输入。**

- **空输入**能抓到：平均值或比例里的除零；对空序列调 `max()`；无内容可报时仍打印了表头；本该*什么都不输出*却打出一个空行。
- **单条记录**能抓到：从第二个元素才开始工作的循环（`for a, b in zip(xs, xs[1:])` 一次都不跑）；那个「首个特殊」的分支同时也是最后一个元素；只在没有相邻元素时才现形的差一错误。
- 对**每个 part** 都跑这两个，不只对完成品 —— part 3 通常会加出 part 1 从未走过的代码路径。
