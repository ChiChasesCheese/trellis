---
id: hl-j04-holder-null
node: java21.j04-record-patterns
type: qa
step: 10
---
## Q
`record Holder(Object value)`，`new Holder(null)` 会匹配 `case Holder(String s)` 吗？会匹配 `case Holder(Object o)` 吗？`Holder` 本身为 `null` 呢？

## A
```java
switch (h) {
    case Holder(String s) -> "string " + s;
    case Holder(Object o) -> "object " + o;
}
```
- `Holder(String s)` **不匹配**：对 `Object` 组件，`String` 不是无条件模式，`null` 不是 `String`。
- `Holder(Object o)` **匹配**，`o` 为 `null`，输出 `object null`，没有 NPE。
- `h` 本身为 `null`：无 `case null` 时抛 **NPE**，不会进入任何 record 模式。
