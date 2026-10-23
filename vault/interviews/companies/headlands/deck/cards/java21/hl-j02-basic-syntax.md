---
id: hl-j02-basic-syntax
node: java21.j02-sealed
type: qa
step: 3
---
## Q
写出一个有 `Ok(long value)` 和 `Err(String message)` 两种结果的 `sealed interface Result`。`permits` 名单和子类的 `implements` 是什么关系？

## A
```java
sealed interface Result permits Ok, Err {}
record Ok(long value) implements Result {}
record Err(String message) implements Result {}
```
- `sealed`：类型被封印，**只有 `permits` 后列出的类型**才允许直接继承 / 实现它。
- **双向确认**：子类名出现在父类的名单里，**同时**子类自己也要写 `implements Result`，缺任何一边都不行。
- `sealed` 可以修饰 `interface`、`class`、`abstract class`。
