---
id: hl-j08-real-style
node: java21.j08-var
type: qa
step: 22
---
## Q
真实代码里 `var` 的使用分寸是什么？举 `OrderBook` 里 `var` 与显式类型混用的例子。

## A
分寸：**引用类型用 `var`，需要"这是 `long`"信息的数值用显式类型**。

```java
var e = book.firstEntry();     // Map.Entry<Long, PriceLevel>，类型很长
var top = opp.firstEntry();
var bad = validate(cmd);       // String，读者要翻 validate 才知道，稍微勉强
long px = top.getKey();        // 数值：显式写 long
long left = sweep(...);        // 数值：显式写 long
```
右边带 `new X<...>()` 的场合（如 `var jobs = new ArrayList<Job>();`、`var byId = new LinkedHashMap<Integer, Job>();`）最适合；record 模式里的 `case Ok(var chains)` 是同一套推导，类型取自组件声明。
