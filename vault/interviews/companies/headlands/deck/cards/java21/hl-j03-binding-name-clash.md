---
id: hl-j03-binding-name-clash
node: java21.j03-pattern-switch
type: qa
step: 23
---
## Q
下面的代码为什么编译不过？怎么改？

```java
String s = "x";
switch (o) { case String s -> ...; default -> ...; }
```

## A
绑定变量**不能与外层已定义的局部变量同名**：`String s` 已经存在，`case String s` 报"变量已定义"。

改个名字即可，如 `case String str ->`。不同分支之间的绑定变量可以重名，但不能和外层作用域里的变量冲突。
