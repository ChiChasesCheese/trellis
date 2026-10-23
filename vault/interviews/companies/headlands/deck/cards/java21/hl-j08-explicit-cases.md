---
id: hl-j08-explicit-cases
node: java21.j08-var
type: qa
step: 18
---
## Q
哪两种情形即使可以用 `var` 也应该显式写类型？

## A
```java
long notional = compute(fills.get(0));       // 显式写 long：读者一眼知道是 long
Map<String, Long> declared = qtyBySymbol;     // 想把变量类型限制成接口时，显式写接口
```
1. **数值类型**：数字类型是业务语义，读者要一眼知道是 `long` 还是 `int`；
2. **希望变量类型是接口 / 父类**：显式类型表达了"只依赖这个接口"。
