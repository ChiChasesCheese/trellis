---
id: pl-abstraction-bounds-variance-unique-use-vs-declaration-site
node: abstraction.bounds-variance
type: qa
step: 8
---
## Q
使用处型变（Java 通配符）与声明处型变（Kotlin、C# 的 `in`/`out`）有什么本质区别？各自适合什么哲学？

## A
**声明处**：类的作者在定义时声明一次，如 `interface Source<out T>`。作者最了解这个类怎么用 `T`，所以由作者承担证明；编译器当场检查，所有使用者免费获得协变，无需任何语法。缺点是类必须在定义时就想好，且一个类要么整体协变，要么不能；像 `List<T>` 这种既读又写的类，只能拆成只读的 `List<out T>` 和可变的 `MutableList<T>`。

**使用处**：类本身不变，每个使用方按自己的需要说「我只读」或「我只写」。灵活：同一个 `List<T>` 在不同函数里可以被当协变、也可以当逆变。缺点是负担转嫁给**每一个调用者和每一个 API**：`Collections.copy(List<? super T> dest, List<? extends T> src)` 这种签名要靠 PECS 才读得懂。

哲学差别：使用处型变相信「作用域越小，信息越准确」，把声明的责任放给用户；声明处型变相信「类型的作者最懂自己的类型」，用类型定义承载信息，让使用者轻松。工业经验偏向后者：Kotlin 在设计时就选声明处，并保留 Java 式使用处作为补充；Scala、C#、Python 3.12 都走声明处或推导。

Java 的选择是历史的：泛型在 2004 年加入时，为了让旧的 `java.util` 集合平滑过渡，没有时间改写所有类的变体声明。这是一个典型的「向后兼容决定了语法」的例子。
