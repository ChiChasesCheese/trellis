---
id: hl-j05-parse-command
node: java21.j05-switch-expressions
type: qa
step: 21
---
## Q
命令解析：怎么用一个 `switch` 表达式把命令名映射成 `sealed` 命令类型的值？老写法有什么风险？

## A
```java
return switch (t[0].toUpperCase(Locale.ROOT)) {
    case "LIMIT" -> {
        need(t, 5);
        yield new Limit(Long.parseLong(t[1]), Side.valueOf(t[2].toUpperCase(Locale.ROOT)),
                Long.parseLong(t[3]), Long.parseLong(t[4]));
    }
    case "CANCEL" -> { need(t, 2); yield new Cancel(Long.parseLong(t[1])); }
    default -> throw new IllegalArgumentException("unknown command: " + t[0]);
};
```
每个分支先检查参数个数再 `yield new ...`。老写法要先 `Command result = null;`，每分支赋值并 `break`，还可能**漏赋值得到 `null`**。
