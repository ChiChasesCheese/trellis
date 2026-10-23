---
id: hl-j01-forbidden-members
node: java21.j01-record
type: qa
step: 7
---
## Q
`record` 里哪些事不允许做？各自的编译错误是什么？

## A
- **声明实例字段**：报 `field declaration must be static (consider replacing field with record component)`。
- **`extends` 别的类**：不行，record 已隐式继承 `java.lang.Record`，Java 只有单继承。
- **被别的类继承**：不行，record 隐式是 `final`。
- **在方法里给字段赋值**：报 `cannot assign a value to final variable x`。
- **额外构造器不先调用 `this(...)`**：报 `constructor is not canonical, so its first statement must invoke another constructor of class P`。

限制是故意的：record 的全部状态就是括号里的组件，编译器才敢自动生成 `equals` / `hashCode` / `toString`。
