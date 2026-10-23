---
id: hl-j04-real-usage
node: java21.j04-record-patterns
type: qa
step: 24
---
## Q
真实代码里 record 模式常见的用法有哪些？写出订单簿 `execute` 里对四种命令的解构。

## A
```java
case Limit(var id, var side, var px, var q) -> { ... }
case Market(var id, var side, var q) -> { ... }
case Cancel(var id) -> { ... }
case Modify(var id, var newQty) -> { ... }
```
其他用法：
- 队列均值渲染：嵌套 record 模式 + 守卫 `case Value(Mean(var n, var d)) when d == 1`；
- 单组件解构 `case And(var m) -> reg & m;`，零组件写 `_`（未命名模式，Java 21 预览）；
- `instanceof` 版：`if (e instanceof Rejected(var id, var why)) { ... }`；
- 泛型：`case Failed<T>(var cause) -> throw ...`、trampoline 的 `case More<T>(var next) -> cur = next.get();`。
