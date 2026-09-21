---
id: for-else-vs-try-else-normal-completion
node: iteration.comprehensions
type: qa
source: python-docs
---
## Q
`for...else` 和 `try...else` 里的 `else` 子句，各自在什么条件下执行？它们的共同点是什么？

## A
`for...else` 的 `else` 在循环把迭代器耗尽、没有被 `break` 提前终止时执行。`try...else` 的 `else` 在 `try` 块没有抛出任何异常、也没有执行 `return`/`continue`/`break` 提前跳出时执行，且 `else` 里新抛出的异常不会被前面的 `except` 子句捕获。两者的共同点：`else` 表达的都是「主体正常走到底、没有被异常或提前退出打断」这个分支，不是常见的「否则」语义。
