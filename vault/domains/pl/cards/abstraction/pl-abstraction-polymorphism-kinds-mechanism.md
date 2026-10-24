---
id: pl-abstraction-polymorphism-kinds-mechanism
node: abstraction.polymorphism-kinds
type: qa
step: 4
---
## Q
三种多态在编译器和运行时里各是怎么落地的？为什么重载和覆写（override）的选择时机不同？

## A
- **特设多态**：编译器看**静态类型**（声明处能推出的类型）选出一个具体函数，之后就是普通的直接调用，运行期没有任何选择。Rust 的 `impl Describe for i32` 也一样，由类型推断选实现。
- **子类型多态**：调用点只知道接口，运行期读对象里的类型信息（虚表指针，`vtable`）再间接跳转。多一次内存读取，也挡住了内联。
- **参数多态**：要么每种类型生成一份代码（单态化），要么只留一份代码、类型信息擦掉。详见泛型实现一节。

同一个 Java 程序里能同时看到前两种的差别：

```java
static void show(Object o) { System.out.println("Object"); }
static void show(String s) { System.out.println("String"); }
Object o = "hi";
show(o);                        // 输出 Object：重载看静态类型
A x = new B();                  // B 覆写了 A.who()
System.out.println(x.who());    // 输出 B：覆写看运行期类型
```

`o` 的运行期类型是 `String`，但重载在编译期就按声明类型 `Object` 定了，所以走 `show(Object)`。覆写是虚方法，要等运行期按对象实际类型选。这条规则让重载可以零成本，也让重载「看起来像多态却不是动态的」。C++ 的规则与 Java 相同：重载按静态类型在编译期选，只有 `virtual` 函数（显式声明才按对象实际类型调用）的覆写在运行期选；模板则每个类型各生成一份代码，是单态化。
