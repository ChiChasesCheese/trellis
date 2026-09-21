---
id: await-reuses-yield-from-suspension-chain
node: iteration.yield-from
type: qa
source: peps
---
## Q
60 秒内讲清楚：`yield from` 和后来的 `async`/`await` 语法是什么关系？

## A
`async`/`await` 是给协程（coroutine）设计的独立语法，但协程在 CPython 内部仍然基于生成器实现；每一次 `await` 最终都会在委托链的某一层通过底层的一次 `yield` 挂起，而这条委托链正是靠 `yield from` 透明传递 `send`/`throw`/`close` 的能力串起来的。没有 `yield from` 先解决好生成器委托、返回值与异常传递的问题，`async`/`await` 就不会有一套现成、已验证的挂起机制可以复用。
