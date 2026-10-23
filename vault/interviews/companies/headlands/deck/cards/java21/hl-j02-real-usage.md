---
id: hl-j02-real-usage
node: java21.j02-sealed
type: qa
step: 23
---
## Q
真实代码里 `sealed` 层级常见的用法有哪些？各举例说明它们把什么写进了类型。

## A
- **结果类型**：`Outcome permits Ok, Malformed`——"分析可能成功也可能失败"，返回类型就是答案，`render` 的 `switch` 不用 `default`。
- **异步轮询**：`Poll<T> permits Ready, Pending, Done`——有值、暂无、已结束三种全写进类型；内部队列消息用 `private sealed interface Msg<T> permits Item, End, Failed`，说明 `sealed` 也可只在类内部使用。
- **溢出**：`SumResult permits Ok, Overflow`——调用方不处理 `Overflow` 就编译不过；`Trampoline<T> permits Done, More`。
- **订单簿**：`Command` / `Event` 两棵树。
- **三层指令**：`Instr` → `Update`（15 种）/ `Query`（3 种），`apply(int reg, Update u)` 只接受 `Update`。
