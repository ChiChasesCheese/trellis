---
id: pl-eng-apidesign-found-context
node: engineering.api-design
type: qa
step: 6
---
## Q
请求 ID、截止时间、取消信号这类“跨层上下文”，该显式地当参数一层层传，还是隐式地绑在当前执行流上？Go 的 `context`、Java 的 `ScopedValue`、Python 的 `contextvars` 各怎么做？

## A
**问题**：一次请求要穿过十几层函数，每层都可能要写日志（要请求 ID）、发下游调用（要截止时间）、响应取消。给每个函数都加一个参数很啰嗦；把它放进全局变量会在并发下互相覆盖；放进线程局部变量（`ThreadLocal`）在协程和虚拟线程场景下又不可靠。

**设计空间**：**显式传递** vs **隐式的执行流绑定**。

**Go：显式。** 约定 `ctx context.Context` 是函数的第一个参数，从入口一路传下去。
```go
func charge(ctx context.Context, cents int) error {
	select {
	case <-time.After(500 * time.Millisecond): return nil
	case <-ctx.Done(): return fmt.Errorf("charge %d: %w", cents, ctx.Err())
	}
}
```
带 100 毫秒截止时间调用，输出 `charge 1299: context deadline exceeded`。代价是每个函数签名都多一个参数；换来的是**数据流在代码里完全可见**，没有魔法。

**Python：隐式。** `contextvars.ContextVar` 绑定到当前执行流；`asyncio` 在创建任务时拷贝当前上下文，所以并发任务互不影响。
```python
req_id = contextvars.ContextVar("req_id", default="-")
async def deep(): print("req_id =", req_id.get())      # no parameter
async def handle(rid): req_id.set(rid); await deep()
await asyncio.gather(handle("r-1"), handle("r-2"))
```
输出 `req_id = r-1`、`req_id = r-2`，而外层看到的仍是默认值 `-`。

**Java：隐式，但有作用域。** JDK 25 中 `ScopedValue` 已正式发布（JEP 506）：`ScopedValue.where(REQ, id).run(task)`，值只在 `run` 内的调用链可见、不可变，离开即解绑；在 2 个虚拟线程里分别绑定 `r-1`、`r-2`，各自读到自己的值，而 `REQ.isBound()` 在作用域外为 `false`。它是 `ThreadLocal` 的替代：不可变、范围明确、对虚拟线程廉价。

**取舍**：
- 显式：容易推理、易测试，但侵入签名；
- 隐式：签名干净，适合横切关注点（追踪 ID、认证信息），但依赖运行时机制，调试时“值从哪来”不直观。

经验：**控制流相关**的（取消、截止时间）适合显式；**纯观测相关**的（日志里的请求 ID）适合隐式。
