---
id: pl-conc-async-await-unique-cancel
node: concurrency.async-await
type: qa
step: 6
---
## Q
给一个 `async` 任务加 50 毫秒的超时后，它被取消时 Rust 和 Python 分别发生什么？为什么说 Rust 的取消「只是丢弃」？

## A
Rust（tokio）：
```rust
async fn job() {
    let _g = Guard;                 // prints on Drop
    println!("job start");
    sleep(Duration::from_secs(10)).await;
    println!("job finished");       // never printed
}
let r = timeout(Duration::from_millis(50), job()).await;
println!("{:?}", r.is_err());
```
输出：`job start`、`job dropped (cancelled)`、`true`。超时到期时，`timeout` 直接把还停在 `sleep().await` 的 `job` future 丢弃（drop）。因为 future 只是一个状态机对象，丢弃就等于取消：不再被 `poll`，局部变量按 `Drop` 逐个清理，`job finished` 永远不会出现。取消点只会在 `await` 处，所以没有强杀线程的问题。

Python：
```python
async def job():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("job got CancelledError"); raise
await asyncio.wait_for(job(), 0.05)
```
输出：`job start`、`job got CancelledError`、`timeout`。Python 向任务内部注入一个 `CancelledError` 异常，代码可以捕获它做清理，也可以吞掉它（吞掉后取消失效）。

对比：Rust 的取消由类型系统保证清理（Drop），但 `Drop` 里不能 `await`；Python 的取消是一种异常，更灵活，也更容易写错。Go 的 goroutine 和 Java 线程没有强制取消手段，只能靠 `context` 或 `interrupt` 协作。
