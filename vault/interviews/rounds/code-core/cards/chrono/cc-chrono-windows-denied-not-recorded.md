---
id: cc-chrono-windows-denied-not-recorded
node: chrono.windows
type: qa
---
## Q
A client is over its limit and keeps retrying. Your limiter appends every arrival to the window. What breaks?

## A
**Rejected events must not enter the window.** If denials are recorded, the window never drains — a client that keeps retrying stays locked out forever, and the stored count stops meaning "requests admitted".

- Append on the *allow* path only. Track "last seen" in a separate scalar if you need idle eviction ([[cc-chrono-windows-per-key-state]]).
- The same rule generalizes: a rejected transfer, a refused acquire, a dropped malformed row must all leave the state they were tested against untouched.
- It also protects the accounting: "how many did we serve" and "how many did they send" are different numbers, and only one of them belongs in the window.
- Test it: burst until denied, wait out the window, one request must then be admitted.

## Q zh
某个客户端超限后不停重试。你的限流器把每一次到达都追加进窗口。会出什么问题？

## A zh
**被拒绝的事件不能进窗口。** 如果把拒绝也记下来，窗口永远排不空 —— 一个不停重试的客户端会被永久锁死，而且存下来的计数不再表示「被放行的请求数」。

- 只在*放行*路径上追加。若需要空闲驱逐，就用一个单独的标量记录「最后一次出现」（[[cc-chrono-windows-per-key-state]]）。
- 同一条规则可以推广：被拒的转账、被拒的加锁、被丢弃的畸形行，都必须让它们所检查的状态保持不变。
- 它也保护了统计口径：「我们服务了多少」和「他们发了多少」是两个数字，只有其中一个属于窗口。
- 测试方法：一直发到被拒，等过窗口时长，此时必须有一个请求被放行。
