---
id: hl-j07-basic-form
node: java21.j07-text-blocks
type: qa
step: 3
---
## Q
文本块（text block）的基本写法的四条规则是什么？`"""abc"""` 会报什么错？写出一个 JSON 例子。

## A
```java
String json = """
        {
          "symbol": "AAPL",
          "qty": 100
        }
        """;
```
1. 开头三个双引号 `"""`，**后面必须直接换行**（可有空格，不能有别的字符）：`"""abc"""` 报 `illegal text block open delimiter sequence, missing line terminator`；
2. 内容从**下一行**开始；
3. 结尾也是 `"""`，可单独一行，也可紧跟最后一行内容；
4. 里面**直接写 `"`**，不用转义。
