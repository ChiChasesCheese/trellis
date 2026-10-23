---
id: hl-j08-non-denotable
node: java21.j08-var
type: qa
step: 13
---
## Q
什么是非可表示类型（non-denotable type）？`var` 对它有什么独特的价值？写一个匿名类的例子。

## A
匿名类、交叉类型这些**无法在源码里写出名字**的类型。`var` 能保留它们：

```java
var anon = new Object() { int hits = 0; void hit() { hits++; } };
anon.hit();                          // 能调用！
```
如果写 `Object anon = new Object() {...}`，`anon.hit()` 编译不过，因为向上转型丢掉了匿名类自己的成员。
