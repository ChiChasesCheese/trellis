---
id: hl-j01-why-boilerplate
node: java21.j01-record
type: qa
step: 2
---
## Q
Java 8 的值对象类里，`private final` 字段、构造器、getter、`equals`、`hashCode`、`toString` 各自为什么必须存在？

## A
- `private final` 字段：保证值稳定、创建后不变。
- 构造器：一次设好所有字段。
- getter：让外部读到私有字段。
- `equals`：默认是**引用比较**，内容相同也不等，必须重写。
- `toString`：默认输出形如 `J01Old$Fill@1b6…86`，看不出内容。
- `hashCode`：和 `equals` 必须配套，否则放进哈希容器会出错。

其中最阴险的是 `equals` / `hashCode`，下一张卡讲它们不配套的后果。
