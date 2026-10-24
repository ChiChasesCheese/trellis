---
id: pl-abstraction-typeclasses-foundation-coherence
node: abstraction.typeclasses
type: qa
step: 6
---
## Q
一致性（coherence）保证了什么？没有它时，同一个集合在不同地方为什么会对「相等」和「顺序」有不同理解，Java 的 `TreeSet` 里能看到什么现象？

## A
**一致性**指：对任何一对（trait, 类型），整个程序里**至多有一个实例**。于是 `a < b` 对 `String` 的含义不会因为你身处哪个模块、导入了什么而改变。Haskell 靠约定和警告，Rust 靠孤儿规则强制（trait 或类型至少一个来自当前 crate）。

没有一致性，「怎样比较」就成了一个**可以随时换的运行时值**。Java 的 `TreeSet` 在构造时接收一个 `Comparator`，它不是类型的一部分，所以静态类型相同的集合可以有完全不同的顺序和相等概念：

```java
TreeSet<String> rev = new TreeSet<>(Comparator.reverseOrder());
rev.addAll(List.of("a", "b", "c"));
TreeSet<String> nat = new TreeSet<>(List.of("a", "b", "c"));
// rev = [c, b, a]   nat = [a, b, c]   both are TreeSet<String>

TreeSet<String> ci = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
ci.add("A");
ci.contains("a");                    // true
new HashSet<>(ci).contains("a");     // false
```

`ci` 认为 `"A"` 和 `"a"` 是同一个元素，把它复制进 `HashSet`（用 `equals`）后，`"a"` 就找不到了。同样的元素，换一个容器，成员判断的结果不同。把 `rev` 和 `nat` 合并时，结果取决于目标集合用的哪个比较器，而类型上看不出来。`TreeSet` 官方文档里也专门提醒：比较器的相等性要与 `equals` 一致，否则集合行为会违反 `Set` 接口。

Rust 的做法：顺序是类型的性质，要换顺序就换类型。

```rust
let nat: BTreeSet<i32> = [1, 2, 3].into_iter().collect();
let rev: BTreeSet<Reverse<i32>> = [1, 2, 3].into_iter().map(Reverse).collect();
// nat = {1, 2, 3}      rev iterates as [3, 2, 1]
```

`BTreeSet<Reverse<i32>>` 与 `BTreeSet<i32>` 是不同的类型，两者不能混用，编译器会拦住。

C++ 不强制一致性：两个源文件对同一个类型写出不同的 `std::hash` 特化，编译器和链接器都不报错（标准把这类违反单一定义规则的错误归为无需诊断），运行时则是未定义行为（标准不规定后果），两边的容器各用各的哈希。一致性靠团队纪律：每个特化只在一个头文件里出现一次。
一致性的代价：你**不能为同一个类型提供两个并存的实例**，也不能为别人的类型实现别人的 trait；想要不同行为只能用 newtype 包装。

这是一个典型的取舍：一致性换来「读代码时一个操作只有一种含义」，付出的是灵活性。Scala 的隐式参数选了另一端，允许局部覆盖实例，更灵活，但同一个值在不同作用域里行为不同，需要读者追踪导入。
