---
id: hl-j07-sql-concat-bug
node: java21.j07-text-blocks
type: qa
step: 2
---
## Q
用字符串拼接写多行 SQL 时，`"FROM fills" + "WHERE side = 'BUY' "` 会得到什么？为什么编译器不报错？文本块怎么避免？

## A
```java
String sql = "SELECT symbol, SUM(qty) " +
        "FROM fills" +                  // ← 少了结尾空格
        "WHERE side = 'BUY' " + ...
```
结果是 `"... FROM fillsWHERE side = 'BUY' ..."`，`fillsWHERE` 粘在一起。编译器看不出来，**数据库执行时才报错**。

文本块里每行自带换行，不会再出现这种粘连。
