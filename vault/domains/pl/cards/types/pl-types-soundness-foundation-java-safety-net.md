---
id: pl-types-soundness-foundation-java-safety-net
node: types.soundness
type: qa
step: 2
---
## Q
Java 的类型系统有已知漏洞，为什么它仍然保证内存安全？「静态检查加运行时安全网」具体由哪些检查组成？

## A
Java 的静态类型系统并不严格可靠：数组协变、泛型擦除、原始类型、`null` 都让「检查通过」不等于「类型正确」。Java 的做法是在虚拟机里**设置多道运行时检查**，保证类型错误不会演变成内存破坏，而是变成确定的异常：

1. **强制转换检查**：`(String) obj` 编译成 `checkcast` 指令，类型不符立即抛 `ClassCastException`。
2. **数组存入检查**：往 `Object[] xs = new String[1]` 存入整数时，JVM 检查元素的真实类型，抛 `ArrayStoreException`。
3. **泛型出口检查**：泛型类型信息在运行时被擦除，但编译器在每个读出泛型值的地方**自动插入** `checkcast`。
4. **空引用检查**：对 `null` 解引用抛 `NullPointerException`，而不是读无效地址。
5. **数组越界检查**。

第 3 条值得亲眼看看。下面的 `pick` 用不受检的转换 `(T) o`，在方法内部**什么也没检查**：

```java
@SuppressWarnings("unchecked")
static <T> T pick(Object o) { return (T) o; }
// Object o = 42;
// String s = pick(o);     // prints "before"; then:
// ClassCastException: class java.lang.Integer cannot be cast to class java.lang.String
```

异常发生在调用者那一行，因为编译器在 `String s = ...` 处插入了转换到 `String` 的检查。`pick` 自己是「说谎」的方法，但谎言在到达使用点时被拆穿。

这样设计的效果是：**类型漏洞的后果被限制为异常，不会读到别的类型的内存**。但错误的位置可能离真正的根源很远（污染在这里，崩溃在那里）。

要记住的事实：Java 的承诺较弱，是「不会破坏内存」，不是「不会出现类型错误」。要尽量靠近编译期，就要少用原始类型、不受检转换和反射，并把 `-Xlint:unchecked` 的警告当作缺陷处理。
