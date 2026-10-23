---
id: hl-ld02-desk-assembly
node: problems.ld02-trading-ood
type: qa
step: 10
---
## Q
`TradingDesk` 怎么装配订单、仓位、风控？`submit`、`onExec`、`replay` 的规则和代码是什么？

## A
每个变更方法**先把输入追加到 journal，再处理**——即使处理会抛异常，输入也已在 journal 里。`handle` 是**唯一**修改状态的地方，`submit/onExec/...` 是「先记日志、再调 handle」的薄包装；`replay` 也调同一个 `handle`——实时与恢复同一份代码，不会悄悄分叉。

`DeskEvent`（sealed）= `Submit`、`SetReferencePrice`、`Halt`、`Resume` 以及 `ExecEvent`，是**全部输入**。
```java
private Object handle(DeskEvent e) {
    return switch (e) {
        case DeskEvent.Submit s -> handleSubmit(s);
        case DeskEvent.SetReferencePrice(var symbol, var px) -> { risk.setReferencePrice(symbol, px); yield null; }
        case DeskEvent.Halt h -> { risk.halt(); yield null; }
        case DeskEvent.Resume r -> { risk.resume(); yield null; }
        case ExecEvent x -> handleExec(x);
    };
}
private RiskResult handleSubmit(DeskEvent.Submit s) {
    Order o = s.order();
    if (orders.contains(o.id())) throw new IllegalArgumentException("duplicate order id " + o.id());
    RiskResult r = risk.check(o, positions, orders);      // 登记之前
    orders.submit(o);
    if (r instanceof RiskResult.Rejected(var reason)) orders.apply(new ExecEvent.Reject(o.id(), reason.name()));
    return r;
}
private boolean handleExec(ExecEvent x) {
    boolean applied = orders.apply(x);
    if (applied && x instanceof ExecEvent.Fill(var orderId, var ignoredExecId, var qty, var px)) {
        Order o = orders.get(orderId).order();
        positions.onFill(o.symbol(), o.side(), qty, px);
    }
    return applied;
}
public static TradingDesk replay(RiskLimits limits, List<DeskEvent> journal) {
    TradingDesk d = new TradingDesk(limits);
    for (DeskEvent e : journal) {
        d.journal.add(e);
        try { d.handle(e); }
        catch (IllegalArgumentException | IllegalStateException | NoSuchElementException | ArithmeticException sameAsBefore) { }
    }
    return d;
}
```
- `submit`：重复 id 抛异常（不改状态）；先 `risk.check`（**登记之前**，否则这张单把自己算进未完成数量）；通过 ⟹ `orders.submit`；被拒 ⟹ **仍然** `orders.submit`，然后立刻应用 `Reject(id, reason.name())`，所以 `order(id)` 是 `REJECTED`，`rejectReason` 是原因枚举名。**这个内部 Reject 不进 journal**（是输出不是输入，重放时由同样的风控重新产生）；
- `onExec`：成功应用的 `Fill` 同步更新 `PositionBook`（订单里的标的和方向，成交里的数量和价格）；重复 `Fill`（返回 false）不更新仓位；
- `replay`：只吞**预期的**业务异常；`NullPointerException`、`OutOfMemoryError` 说明有 bug，应让它崩；结果的 `allOrders()`、`position(s)`、`journal()` 与原 desk 逐项相等；
- `journal()` 返回 `List.copyOf` 快照，之后的操作不改变已取出的列表（返回内部 list 是常见 bug）。
