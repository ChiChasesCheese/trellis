---
id: pl-abstraction-typeclasses-foundation-haskell-dictionary
node: abstraction.typeclasses
type: qa
step: 2
---
## Q
Haskell 的类型类（typeclass）由哪几部分组成？编译器怎样用「字典传递」实现 `Ord a =>` 这样的约束？

## A
Haskell 的类型类有三个部分：

1. **类声明**（class）：一组方法的签名，描述「能力」。比如 `Ord`（可排序）声明了 `compare`、`<=` 等方法。
2. **实例声明**（instance）：说明某个具体类型怎样实现这个能力。`instance Ord Int` 给出整数的比较实现；实例可以写在类型定义之外，甚至在别的模块。
3. **约束**（constraint）：写在类型签名里，`maxOf :: Ord a => a -> a -> a` 读作「对任何有 `Ord` 实例的类型 `a`，函数从两个 `a` 得到一个 `a`」。

Haskell 编译器的实现方式叫**字典传递**（dictionary passing）：每个实例被编译成一个记录（字典），里面是该类型对该类的所有方法实现。带约束的函数被改写成**多一个字典参数**的普通函数：

```text
maxOf :: Ord a => a -> a -> a
   ==>  maxOf dOrd x y = if (<=) dOrd y x then x else y      (conceptually)
```

调用 `maxOf 3 7` 时，编译器看到类型是 `Int`，找到 `Ord Int` 的字典，自动补成 `maxOf ordIntDict 3 7`。程序员写的代码里没有字典，是编译器代填的。

对比 Java：

```java
static <T> T maxOf(T a, T b, Comparator<T> ord)   // you pass the "dictionary"
```

`Comparator<T>` 就是一个手写的字典。区别只在谁来传：Haskell 由编译器按类型推出来，Java 由调用者显式传。

这带来类型类的两个重要性质：

- **实现按类型选择**，而不是按运行时对象选择。同一个值不需要「携带」自己的方法表，原始的 `Int` 也可以有实例，不必装箱成对象。
- **可以按返回类型分派**：`minBound :: Int`、`read "5" :: Int` 没有任何参数，仍可以依据期望的类型选实例。OOP 的虚方法依赖接收者对象，做不到这一点。

Rust 的 trait 在语义上是同一族概念，编译方式则以单态化为主：为每个具体类型生成一份专门的代码，字典在编译期就被消去。
