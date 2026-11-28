---
id: pl-out-java-dispatch-field-hiding
node: output.java-dispatch
type: qa
step: 2
---
## Q
**字段不多态**｜读代码说输出

```java
class A {
    String n = "A";
    String get() { return "A"; }
    String show() { return n + get(); }
}
class B extends A {
    String n = "B";
    String get() { return "B"; }
}
public class Main { public static void main(String[] x) {
    A a = new B();
    System.out.println(a.n);
    System.out.println(a.get());
    System.out.println(((B) a).n);
    System.out.println(a.show());
} }
```

输出什么？

## A
**输出。**
```
A
B
B
AB
```

**为什么。**
- 方法调用是虚的：`a.get()` 按对象实际类型 `B`，输出 B。
- 字段不是：`a.n` 按声明类型 `A` 取，得 A。`B` 里的 `n` 只是另一个同名字段（隐藏，hiding），对象里同时有两个 `n`；`((B) a).n` 才是 B。
- `show()` 写在 `A` 里，里面的 `n` 编译期就绑到 `A.n`，而 `get()` 是虚的，所以是 "A" + "B"。

**语言为什么这样设计。**
- 字段访问编译成固定偏移的读取，对象布局在编译期就定了，所以快；让字段也多态需要多一层间接。JLS 8.3 因此把同名字段规定为「隐藏」而不是「重写」。
- Python 的属性按名字在实例字典里查，不存在「同名的两个字段」；C# 和 Kotlin 的属性（property）实际是 getter 方法，可以重写。

**怎么写才对。**
```java
String name() { return "A"; }      // 暴露方法，子类重写
// 子类里不要再声明同名字段
```

**面试里一句话。**
Methods dispatch on the runtime class but fields resolve on the static type, so hiding a field is not overriding it.
