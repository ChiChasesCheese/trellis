---
id: hl-ld02-types-record-sealed
node: problems.ld02-trading-ood
type: qa
step: 11
---
## Q
这个设计怎么「用类型表达不变量」？写出 `Order` 的紧凑构造器、`ExecEvent` 的 sealed 层级，以及相关的 Java 21 特性用法。

## A
让非法值**无法构造**，由编译器 / 构造器拦，而非靠每个方法记得检查。
```java
public enum Side { BUY, SELL }                  // 不是字符串，sign(): BUY=+1，SELL=-1
public record Order(long id, String symbol, Side side, long qty, long px) {
    public Order {
        Objects.requireNonNull(symbol, "symbol");
        Objects.requireNonNull(side, "side");
        if (id <= 0) throw new IllegalArgumentException("id must be > 0: " + id);
        if (symbol.isBlank()) throw new IllegalArgumentException("symbol is blank");
        if (qty <= 0) throw new IllegalArgumentException("qty must be > 0: " + qty);
        if (px <= 0) throw new IllegalArgumentException("px must be > 0: " + px);
    }
}
public sealed interface ExecEvent extends DeskEvent permits ExecEvent.Ack, ExecEvent.Fill, ExecEvent.Cancel, ExecEvent.Reject {
    long orderId();
    record Ack(long orderId) implements ExecEvent {}
    record Fill(long orderId, long execId, long qty, long px) implements ExecEvent { /* 紧凑构造器校验 */ }
    record Cancel(long orderId) implements ExecEvent {}
    record Reject(long orderId, String reason) implements ExecEvent { /* reason 非 null */ }
}
```
- 紧凑构造器无参数列表，直接写校验，字段赋值由编译器在末尾补上；`requireNonNull` 抛 NPE，其余抛 `IllegalArgumentException`。
- `sealed ... permits`：只有这四个实现，`apply` 里的 `switch` 穷尽——新增回报不改 switch 就编译不过；`ExecEvent extends DeskEvent`：回报也是 desk 的输入事件。
- **record**：非法对象造不出来；自带结构相等，测试可直接比较两个 desk 的状态（含嵌套 record 递归；含 `double`/数组有陷阱）；不用于需继承或可变处。
- **switch 模式匹配 + record 模式**：不需 `default` 和强转，`case DeskEvent.SetReferencePrice(var symbol, var px)`、`x instanceof ExecEvent.Fill(var orderId, …)`；加 `default` 反会掩盖「新增事件类型忘了处理」。
- **switch 表达式 + `yield`**：无 fall-through，每个分支必须给出值。
- `Math.*Exact` 溢出抛异常；`Stream.toList()` 不可变、`List.copyOf` 防御性拷贝（元素不能 null）；`var` 只在右边已写出类型时用。

旧写法对比：字符串 `side="buy"` 拼错、`equals` 不匹配、编译器不提醒；`double` 数量 0.1+0.2 导致订单永不到 FILLED。
