---
id: pl-abstraction-generics-implementation-foundation-java-erasure
node: abstraction.generics-implementation
type: qa
step: 2
---
## Q
Java 的类型擦除（type erasure）具体擦掉了什么？它让哪些写法变得不可能？

## A
编译器检查完类型后，把泛型信息从字节码里**抹掉**：`T` 变成它的上界（无上界就是 `Object`），在读取处插入强制类型转换。`List<String>` 与 `List<Integer>` 在运行期是同一个类：

```java
new ArrayList<String>().getClass() == new ArrayList<Integer>().getClass()  // true
```

因为运行期没有 `T`，下面这些都不可能，编译器直接拒绝：

```java
class Er2<T> {
    boolean is(Object o) { return o instanceof T; }   // error: Object cannot be safely cast to T
    T make()             { return new T(); }          // error: unexpected type
}
static void g(List<String> l)  {}
static void g(List<Integer> l) {}   // error: name clash: have the same erasure
```

此外泛型参数不能是基本类型：`List<int>` 非法，必须用 `List<Integer>`，每个元素是一个堆上的 `Integer` 对象（带对象头，约 16 字节）加一个引用。

擦除的出发点是迁移兼容（migration compatibility）：2004 年的 Java 5 要求旧的、没有泛型的类库和新代码二进制互通，擦除让一个 `List` 既能被旧代码当原始类型使用，又能被新代码当 `List<String>`。这是用运行期信息换来的生态连续性。
