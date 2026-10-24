---
id: pl-binding-names-scope-foundation-java-locals
node: binding.names-scope
type: qa
step: 5
---
## Q
Java 对局部变量的遮蔽怎样限制？为什么 lambda 只能捕获「事实上的 final」（effectively final）变量？

## A
Java 是块级词法作用域，但**禁止局部变量遮蔽局部变量**（包括形参），只允许局部变量遮蔽字段：

```java
int z = 1;
int z = 2;   // error: variable z is already defined in method main(String[])
```

```java
class Sc { int x = 1;
  void m() { int x = 2; System.out.println(x + " " + this.x); } }  // 2 1
```

字段被遮蔽时还能用 `this.x` 取回，所以允许；局部变量被遮蔽后无法再引用，所以禁止。这是 Java「宁可啰嗦也不留歧义」的取向：Go 和 Rust 把这个风险留给程序员，Java 在编译器里堵死。

**lambda 捕获**的规则更严：被 lambda（或匿名类）引用的局部变量必须是 `final`，或者虽然没写 `final` 但从未被重新赋值（effectively final）：

```java
int n = 0;
n++;
Runnable r = () -> System.out.println(n);
// error: local variables referenced from a lambda expression
//        must be final or effectively final
```

原因是实现方式：lambda 可能在方法返回后、甚至在别的线程里运行，而局部变量活在方法的栈帧上。Java 的做法是把变量的**值复制**进 lambda 对象；如果允许之后再修改，两份值就会不同步。规定不可变，复制就等价于共享。

想要「可变计数器」就必须显式把可变性放进堆上的对象：`AtomicInteger`、`int[1]` 数组。对比 Python 的 `nonlocal`：Python 的闭包捕获的是变量本身（一个 cell），因此可以改。
