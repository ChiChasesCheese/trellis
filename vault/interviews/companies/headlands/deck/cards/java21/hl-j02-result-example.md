---
id: hl-j02-result-example
node: java21.j02-sealed
type: qa
step: 14
---
## Q
补全代码：用 `switch` 表达式把 `sealed interface Result permits Ok, Err` 渲染成字符串，不写 `default`。为什么返回 `Result` 比返回 `null` 或抛异常表示失败更好？

## A
```java
static String show(Result r) {
    return switch (r) {
        case Ok ok -> "ok " + ok.value();
        case Err err -> "err " + err.message();
    };
}
```
编译器知道只有 `Ok` 和 `Err`，所以不需要 `default`。

好处：`Result` 把"可能失败"写进**返回类型**，调用方**不得不**处理 `Err`。另外 `Ok.class.isSealed()` 是 `false`：`record` 隐式 `final`，不是 `sealed`。
