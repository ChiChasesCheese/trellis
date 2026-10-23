---
id: hl-c01-value-semantics
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 1
---
## Q
C++ 的值语义（value semantics）和 Java 的对象变量有什么根本区别？`Point b = a;` 分别发生什么？

## A
- **Java**：`Point p` 只是一个**引用**（reference），`new Point(1,2)` 永远在堆上；`Point b = a;` 复制的是引用，两个变量指向**同一个对象**。
- **C++**：变量**就是**对象本身（那块内存）。`Point b = a;` 造出第二个**独立**的 `Point`，改 `b.x` 不影响 `a.x`。
- 想要 Java 那种「同一对象的另一个名字」，必须显式写引用 `Point& r = a;`（引用 = 已有对象的别名，不是新对象），之后 `r.x = 7` 会改到 `a`。
- 后果：复制成本是显式的（大对象要用引用或移动避免复制），但布局连续、没有对象头，这是 C++ 快的根源。
