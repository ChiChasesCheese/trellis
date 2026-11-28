---
id: pl-out-java-init-instance-order
node: output.java-init
type: qa
step: 3
---
## Q
**实例初始化与 this(...)**｜读代码说输出

```java
class C {
    int x = log("x");
    { log("block"); }
    int y = log("y");
    C() { this(1); log("C()"); }
    C(int n) { log("C(int)"); }
    static int log(String s) { System.out.println(s); return 0; }
}
public class Main { public static void main(String[] a) {
    new C();
} }
```

输出什么？

## A
**输出。**
```
x
block
y
C(int)
C()
```

**为什么。**
- `new C()` 进入 `C()`，它第一行是 `this(1)`，于是转去 `C(int)`。
- 字段初始化和实例块不在 `C()` 里运行，而是在最终调用 `super` 的那个构造器 `C(int)` 的开头，按源码顺序：x、block、y。
- 之后 `C(int)` 的构造器体打印，返回到 `C()` 再打印 `C()`；初始化只执行一次，不会因为 `this(1)` 重复。

**语言为什么这样设计。**
- JLS 12.5 规定：以 `this(...)` 开头的构造器不运行字段初始化，只有直接调用 `super` 的那个构造器运行一次。这样构造器互相委托（constructor chaining）是安全的。
- Python 没有字段初始化，全在 `__init__` 里按代码顺序；C++ 的成员初始化列表按成员声明顺序执行，而不是列表里写的顺序。

**怎么写才对。**
```java
C() { this(1); }            // 其他构造器委托给主构造器
C(int n) { … }              // 初始化集中在一处
```

**面试里一句话。**
Field initializers and instance blocks run in source order once, at the start of the constructor that calls super, not on every this(...) hop.
