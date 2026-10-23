---
id: hl-j07-three-lines-one
node: java21.j07-text-blocks
type: qa
step: 15
---
## Q
补全代码：写一个文本块，源码里是三行 `a`、`b`、`c`，但字符串里是同一行 `"abc"`，没有换行也没有空格。

## A
```java
String s = """
        a\
        b\
        c""";    // "abc"
```
`\` 紧跟换行是**续行转义**，不产生换行；结束符紧跟在 `c` 后面，所以也没有结尾的 `\n`。
