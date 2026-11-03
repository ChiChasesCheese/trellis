---
id: craft-external-call-outside-the-lock-4-across-problems
node: craft.patterns.external-call-outside-the-lock
type: qa
step: 4
---
## Q
**外部调用不持锁 · 订票、熔断器、缓存里的三段式**｜模式

订票的 `confirm`、熔断器的 `call`、缓存的 `get_or_load` 都要调用一个自己控制不了的东西（支付、下游服务、回源函数）。它们各自把「占位—调用—提交」落在哪几行？

## A
**要点。** 同一个三段：锁内拿到许可（占位）→ 锁外调用 → 锁内回报结果。变的是占位的形式：座位是持有凭证，熔断器是「许可 + 代号」，缓存是「领跑者」。

```python
# movie-booking.confirm：延长持有期 → 锁外付款 → 锁内落单
hold = show.extend_hold(hold, self._payment_window)
approved = pay(hold.user_id, amount)          # 不持任何锁
try:
    show.commit(hold, booking_id)
except HoldExpiredError as exc:
    raise HoldExpiredError("... refund ...") from exc

# api-circuit-breaker.call：拿许可 → 调下游 → 回报
gen = self._acquire()          # 不持锁调用下游：慢调用不能把所有线程锁住
...                            # 调 fn，再把结果连同 gen 一起回报

# ttl-cache.get_or_load：领跑者在锁外回源
value = loader()
self.put(key, value, ttl)
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

不变：外部调用一行一定不在 `with lock` 里；变化：占位的凭证不同，失败的补救不同（释放座位、记一次失败、唤醒等待者）。

**见于。** movie-booking、idempotent-transfer（风控 `on_execute` 在占键后、动钱前，两把锁都不持）、ttl-cache、api-circuit-breaker、logger。

**信号。** 一个临界区里出现了网络、磁盘、回调、会阻塞的队列操作，或你不控制的函数调用；以及「拿到许可之后世界可能变了」的窗口。
