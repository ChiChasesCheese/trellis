---
id: pl-out-java-dispatch-static-private
node: output.java-dispatch
type: qa
step: 3
---
## Q
**static 与 private**｜读代码说输出

```java
class A {
    static String who() { return "A"; }
    String me() { return "A"; }
    private String p() { return "A.p"; }
    String callP() { return p(); }
}
class B extends A {
    static String who() { return "B"; }
    String me() { return "B"; }
    private String p() { return "B.p"; }
}
public class Main { public static void main(String[] x) {
    A a = new B();
    System.out.println(a.who());
    System.out.println(a.me());
    System.out.println(a.callP());
    System.out.println(((B) a).who());
} }
```

输出什么？

## A
**输出。**
```
A
B
A.p
B
```

**为什么。**
- `a.who()`：静态方法属于类，不属于对象；编译器看 `a` 的声明类型 `A`，直接绑到 `A.who`（隐藏，不是重写）。`((B) a).who()` 声明类型是 `B`，得 B。
- `a.me()` 是普通实例方法，被重写，运行时按对象选，得 B。
- `private` 方法对子类不可见，不能被重写：`callP()` 写在 `A` 里，调的就是 `A.p`；`B` 里的 `p` 是毫不相关的新方法。

**语言为什么这样设计。**
- static 和 private 调用没有「接收者」参与选择，编译器可以直接绑定（invokestatic、invokespecial）甚至内联；JLS 8.4.8 规定只有可访问的实例方法才能被重写，私有细节不会被子类意外改变。
- C++ 的非 virtual 方法同样按静态类型绑定；Python 没有强制的 private，`_p` 只是约定，按名字查，子类定义同名方法就会覆盖。

**怎么写才对。**
```java
A.who();                    // 静态方法用类名调用
@Override String me() {…}   // @Override 让编译器确认真的在重写
```

**面试里一句话。**
Static and private methods are bound at compile time, so they can be hidden but never overridden.
