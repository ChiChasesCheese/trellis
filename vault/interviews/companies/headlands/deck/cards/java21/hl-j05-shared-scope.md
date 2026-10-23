---
id: hl-j05-shared-scope
node: java21.j05-switch-expressions
type: qa
step: 3
---
## Q
老式冒号 `switch` 里，不同 `case` 声明的变量有什么作用域问题？举例。

## A
整个 `switch { ... }` 是**一个花括号块**，不同 `case` 里声明的变量彼此可见：

```java
case 1:
    String a = "one";
    return a;
case 2:
    a = "two";        // 能用，但 a 在这里根本没有被初始化过！
```
这容易引入"用了没初始化的变量"的隐患。箭头形式让**每个分支自己一个作用域**，消除了这个问题。
