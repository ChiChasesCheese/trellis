---
id: hl-j07-line-continuation
node: java21.j07-text-blocks
type: qa
step: 9
---
## Q
补全代码：用文本块的续行转义把 `SELECT symbol, SUM(qty) FROM fills WHERE side = 'BUY'` 拆成三行写，结果仍是一行。再写一个保住行尾 3 个空格的例子。

## A
```java
String longLine = """
        SELECT symbol, SUM(qty) \
        FROM fills \
        WHERE side = 'BUY'""";
// -> "SELECT symbol, SUM(qty) FROM fills WHERE side = 'BUY'"      一行

String keepTrailing = """
        x\s\s\s
        y""";
// -> "x   \ny"
```
`\` 紧跟换行是续行，不产生 `\n`；注意前面要自己留好空格。`\s` 保住行尾空格。
