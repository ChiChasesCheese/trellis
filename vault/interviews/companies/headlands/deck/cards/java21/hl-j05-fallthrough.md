---
id: hl-j05-fallthrough
node: java21.j05-switch-expressions
type: qa
step: 2
---
## Q
下面的代码对 `Side.BUY` 返回什么？为什么编译器不报错？

```java
switch (s) {
    case BUY:  label += "buy";
    case SELL: label += "sell"; break;
    default:   label += "other";
}
```

## A
返回 **`"buysell"`**，而不是 `"buy"`。

匹配到 `BUY` 后从这里一路往下执行，直到遇到 `break`；`BUY` 分支没有 `break`，就掉进 `SELL`。

编译器不报错，因为 **fall-through 是合法特性**（C 语言传下来的）。这类 bug 评审时很难看出：少一行 `break`，缩进依旧是对的。修法：加 `break;`，或改用箭头形式。
