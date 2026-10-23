---
id: hl-j01-javap-structure
node: java21.j01-record
type: qa
step: 14
---
## Q
用 `javap` 反编译 `record Fill(String symbol, long priceTicks, long qty) {}`，会看到编译器生成了哪些成员？

## A
- 类是 **`final class ... extends java.lang.Record`**（所有 record 的父类，几乎什么都不放的抽象类；类 `final` 不能被继承）。
- 每个组件一个 **`private final` 字段**。
- **规范构造器**，访问级别与 record 本身一致（`public record` 的构造器就是 `public`）。
- 每个组件一个 **`public` 访问器**，名字就是组件名。
- **`toString` / `hashCode` / `equals`**，都是 `final`，方法体只有一条 `invokedynamic`。
