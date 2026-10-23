---
id: hl-j02-private-sealed-record-fill
node: java21.j02-sealed
type: qa
step: 25
---
## Q
补全代码：用 `sealed interface` 和三个 `record` 表示事件 `Rested(long id, long px, long qty)`、`Cancelled(long id)`、`Rejected(long id, String why)`。

## A
```java
sealed interface Event permits Rested, Cancelled, Rejected {}
record Rested(long id, long px, long qty) implements Event {}
record Cancelled(long id) implements Event {}
record Rejected(long id, String why) implements Event {}
```
要点：
- `permits` 名单与每个 `implements Event` 是**双向确认**；
- `record` 隐式 `final`，不用再写修饰符；
- 之后对 `Event` 做 `switch` 无需 `default`。
