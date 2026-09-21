---
id: finally-cleanup-runs-on-cancellation
node: asyncio.cancellation
type: qa
source: python-docs
---
## Q
为什么官方建议协程用 `try/finally`（而不是只用 `try/except`）来做取消时的清理（cleanup）逻辑？

## A
`CancelledError` 会在 `await` 处被抛入协程，`finally` 块无论异常有没有被显式 `except` 捕获都会执行，能保证资源释放、连接关闭等清理逻辑总是跑到；如果显式捕获了 `CancelledError`，清理完成后通常应该把它重新 `raise` 出去，而不是就地吞掉，否则会打乱取消请求原本要传达的「这里要停止」的语义。
