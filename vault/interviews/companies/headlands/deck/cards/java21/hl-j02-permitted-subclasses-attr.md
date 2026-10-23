---
id: hl-j02-permitted-subclasses-attr
node: java21.j02-sealed
type: qa
step: 10
---
## Q
`sealed` 在 class 文件里怎么表示？这份名单由谁检查？

## A
class 文件（Java 17 起）新增 **`PermittedSubclasses` 属性**，一个类名列表。`javap -v` 看 `sealed interface Result permits Ok, Err` 会看到：

```
PermittedSubclasses:
  J02Ex1$Ok
  J02Ex1$Err
```
这份名单**不只由 `javac` 检查，运行时由 JVM 自己检查**：
- 编译不在名单里的子类，`javac` 报 `class is not allowed to extend sealed class: S (as it is not listed in its 'permits' clause)`；
- 绕过 `javac`，JVM 在**加载子类**时拒绝（见下一张卡）。
