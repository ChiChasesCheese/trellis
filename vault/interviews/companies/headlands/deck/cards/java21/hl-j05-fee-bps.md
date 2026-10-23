---
id: hl-j05-fee-bps
node: java21.j05-switch-expressions
type: qa
step: 23
---
## Q
补全代码：手续费 `feeBps(Liquidity liq, long notional)`：`MAKER` 返回 -2（返佣）；`TAKER` 基础 3，成交额小于 10_000 时加 2。三个调用 `(MAKER,5000)`、`(TAKER,5000)`、`(TAKER,2_000_000)` 各返回多少？

## A
```java
static int feeBps(Liquidity liq, long notional) {
    return switch (liq) {
        case MAKER -> -2;               // 做市方返佣
        case TAKER -> {
            int base = 3;
            int surcharge = notional < 10_000 ? 2 : 0;
            yield base + surcharge;
        }
    };
}
```
返回 **-2、5、3**。一行表达式用箭头，需要多条语句的分支用块 + `yield`。
