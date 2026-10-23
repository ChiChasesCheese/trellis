---
id: hl-j01-illegal-states
node: java21.j01-record
type: qa
step: 20
---
## Q
"让非法状态无法表示"（make illegal states unrepresentable）在 `record` 里怎么做到？举 `Order` 的例子，并说明带来什么好处。

## A
在**紧凑构造器**里校验和规范化：`id`、`priceTicks`、`qty` 必须为正，`side` 不能为 null，`symbol` 去空白并转大写。

```java
Order {
    if (id <= 0) throw new IllegalArgumentException("id must be positive: " + id);
    if (qty <= 0) throw new IllegalArgumentException("qty must be positive: " + qty);
    symbol = symbol.strip().toUpperCase();
}
```
例：`new Order(7, " aapl ", ...)` 得到的 `symbol` 是 `"AAPL"`；`id` 为 0 直接抛异常。

好处：**非法的值根本造不出来**。拿到 `Order` 就知道 `qty > 0`，不必处处重检。
