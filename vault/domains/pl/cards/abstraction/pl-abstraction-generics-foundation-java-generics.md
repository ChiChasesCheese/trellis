---
id: pl-abstraction-generics-foundation-java-generics
node: abstraction.generics
type: qa
step: 2
---
## Q
Java 的泛型长什么样？类型参数、有界类型参数和菱形运算符分别是什么，不加约束会怎样？

## A
在类名或方法名后面的尖括号里声明**类型参数**，用到它的地方都是同一个类型：

```java
List<String> names = new ArrayList<>();   // <> 是菱形：右边的类型参数由编译器推断
static <T extends Comparable<T>> T max(List<T> xs) {   // 有界类型参数
    return Collections.max(xs);
}
max(List.of(3, 9, 2));   // 9
```

`T extends Comparable<T>` 是**上界**（bound）：规定 `T` 必须是能和自己比较的类型。函数体里只允许对 `T` 做这个上界允许的操作。不加约束时，`T` 只能当 `Object` 用：

```java
static <T> boolean bigger(T a, T b) { return a > b; }
// error: bad operand types for binary operator '>'
```

Java 泛型的前提是向后兼容：泛型是 Java 5 才加入的，要求旧代码和旧字节码继续运行，因此泛型只在编译期存在，运行期被擦除成 `Object`（详见泛型实现一节）。这也造成两个后果：类型参数不能是基本类型（`List<int>` 不行，要用 `List<Integer>`，会装箱），以及保留了「原始类型」（raw type，`List` 不带参数）这个后门，让旧代码能编译但放弃了类型检查。
