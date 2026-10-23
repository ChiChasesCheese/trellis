---
id: hl-j01-accessor-tostring
node: java21.j01-record
type: qa
step: 5
---
## Q
`record Fill(String symbol, long priceTicks, long qty)` 的访问器怎么调用？`toString()` 输出什么格式？能不能当序列化格式用？

## A
```java
Fill a = new Fill("AAPL", 18_950, 100);
a.symbol();       // "AAPL"，访问器没有 get 前缀
a.toString();     // Fill[symbol=AAPL, priceTicks=18950, qty=100]
a.equals(new Fill("AAPL", 18_950, 100));   // true，按内容比较
```

`toString` 用**方括号**。规范只要求包含所有组件名和值，不固定格式，**别拿它当序列化格式**。
