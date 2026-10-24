---
id: pl-abstraction-bounds-variance-foundation-variance-basics
node: abstraction.bounds-variance
type: qa
step: 2
---
## Q
为什么 `List<Cat>` 不能随意当作 `List<Animal>` 使用？Java 的数组协变是怎样出事的？

## A
假设 `Cat` 和 `Dog` 都是 `Animal` 的子类，且允许把 `List<Cat>` 当作 `List<Animal>`：

1. 有人持有一个 `List<Cat>`，把它传给一个接受 `List<Animal>` 的函数；
2. 函数里往列表加了一个 `Dog`（对 `Animal` 列表合法）；
3. 原持有者回头从 `List<Cat>` 里取出元素，拿到了一只 `Dog`，类型被破坏。

问题出在**写入**。只读的容器（只能取元素）可以协变，可写的容器必须不变。

Java 的数组却被设计成协变的（Java 1.0 没有泛型，需要让 `Object[]` 通用），于是这个漏洞要靠运行期补：

```java
Object[] xs = new String[1];
xs[0] = 42;      // 编译通过
// 运行期：java.lang.ArrayStoreException: java.lang.Integer
```

每次往数组存对象，JVM 都要检查元素的真实类型，既有运行期开销，也把错误从编译期推迟到运行期。Java 的泛型集合吸取教训，做成不变的：`List<Integer> ints; List<Number> ns = ints;` 编译报 `List<Integer> cannot be converted to List<Number>`。

函数类型有相反的规律：能处理任意 `Animal` 的函数，也能处理 `Cat`，所以 `Handler<Animal>` 可以替代 `Handler<Cat>`，这是**参数位置逆变**。简记：作为输出（返回值、读取）协变，作为输入（参数、写入）逆变。
