---
id: hl-j01-compact-ctor-write
node: java21.j01-record
type: qa
step: 10
---
## Q
补全代码：给 `record Order(long id, String symbol, long qty)` 写紧凑构造器（compact constructor），要求 `id > 0`、`qty > 0` 否则抛 `IllegalArgumentException`，并把 `symbol` 去空白后转大写。

## A
```java
record Order(long id, String symbol, long qty) {
    Order {                                     // Order 后面没有 (...)
        if (id <= 0) throw new IllegalArgumentException("id must be positive: " + id);
        if (qty <= 0) throw new IllegalArgumentException("qty must be positive: " + qty);
        symbol = symbol.strip().toUpperCase();  // 给「参数」重新赋值
    }
}
```
紧凑构造器**省掉参数括号**，函数体末尾由编译器**自动把参数赋给同名字段**。所以改写入值就是改参数。
