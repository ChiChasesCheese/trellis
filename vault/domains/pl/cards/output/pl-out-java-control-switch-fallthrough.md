---
id: pl-out-java-control-switch-fallthrough
node: output.java-control
type: qa
step: 3
---
## Q
**switch 穿透**｜读代码说输出

```java
public class Main { public static void main(String[] x) {
    int n = 2;
    switch (n) {
        case 1: System.out.println("one");
        case 2: System.out.println("two");
        case 3: System.out.println("three"); break;
        default: System.out.println("other");
    }
    String r = switch (n) { case 1 -> "one"; case 2 -> "two"; default -> "other"; };
    System.out.println(r);
} }
```

输出什么？

## A
**输出。**
```
two
three
two
```

**为什么。**
- 传统的 `case X:` 只是跳转标签：匹配后从该行一路往下执行，直到遇到 `break` 或 `switch` 结束。
- `n = 2` 命中 `case 2`，没有 `break`，继续执行 `case 3` 的语句，到 `break` 才停；`default` 不会执行，所以输出 two、three。
- 箭头形式 `case 2 ->` 没有穿透（fall through），每个分支独立；`switch` 表达式还要求覆盖所有情况并产生一个值。

**语言为什么这样设计。**
- 穿透来自 C：case 只是 goto 标签，多个值可以共享一段代码。Java 为了兼容 C 家族的写法保留了它，Java 14 才加入箭头语法和 `switch` 表达式。
- Go 默认不穿透，要写 `fallthrough`；Rust 的 `match` 和 Python 3.10 的 `match` 从不穿透。

**怎么写才对。**
```java
switch (n) {
    case 1, 2 -> System.out.println("low");   // 多个值共用，不会穿透
    default   -> System.out.println("other");
}
```

**面试里一句话。**
Colon-style switch cases fall through until a break; arrow-style cases never do.
