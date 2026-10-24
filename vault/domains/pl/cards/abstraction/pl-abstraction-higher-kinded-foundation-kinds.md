---
id: pl-abstraction-higher-kinded-foundation-kinds
node: abstraction.higher-kinded
type: qa
step: 2
---
## Q
类型的「种类」（kind）是什么？为什么说 `Vec` 本身不是一个类型，而 `Vec<i32>` 才是？

## A
值有类型：`3` 的类型是 `i32`。类型也有自己的「类型」，叫**种类**（kind），记作 `*`（读作 type）或箭头形式：

- `i32`、`String`、`Vec<i32>`：种类是 `*`。它们是完整的类型，可以直接有值。
- `Vec`、`Option`：种类是 `* -> *`。它们是**类型构造器**，像一个函数：给它一个类型，才得到一个完整的类型。`Vec` 加 `i32` 得到 `Vec<i32>`。
- `Result`、`HashMap`：种类是 `* -> * -> *`，要两个类型实参。

因此 `Vec` 单独不是一个类型，不能用来声明变量，编译器会明确拒绝：

```rust
let x: Vec = Vec::new();
```

```console
error[E0107]: missing generics for struct `Vec`
  expected at least 1 generic argument
```

普通泛型允许你写 `fn f<T>(x: T)`：`T` 的种类是 `*`，只能代表完整的类型。高阶类型要允许的是 `fn f<F>(x: F<i32>)` 这样的写法：`F` 的种类是 `* -> *`，它代表 `Vec` 或 `Option` 本身，随后才被实参 `i32` 填满。

比较一下三个层次：

| 层次 | 例子 | 抽象的是 |
|---|---|---|
| 值 | `3`、`"a"` | 普通函数的参数 |
| 类型 | `i32`、`Vec<i32>` | 泛型函数的类型参数 `T` |
| 类型构造器 | `Vec`、`Option` | 高阶类型的参数 `F` |

和函数的类比很准确：普通函数对值抽象，泛型对类型抽象，HKT 对类型构造器抽象。每向上一层，抽象更彻底，语言实现和类型检查的难度也上一个台阶（需要对种类做推导和检查，类型之间的相等判断也复杂得多）。

在 Java、Go、Python 里，类型构造器（`List`、`Optional`、`list`）也存在，只是没有一种写法能把它们作为参数传给泛型。C++ 有这种写法：模板模板参数 `template <template <class> class F>`，`F` 就是 `vector` 或 `optional` 本身。
