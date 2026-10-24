---
id: pl-abstraction-higher-kinded-mechanism-gat-functor
node: abstraction.higher-kinded
type: qa
step: 5
---
## Q
Rust 怎样用泛型关联类型（GAT）编码出 `Functor`？这样写出的通用函数是什么样，笨重在哪里？

## A
思路：没有办法直接让 trait 的参数是「类型构造器」，但可以让**实现者自己说出**「把元素类型换成 `B` 之后的同类容器是什么」。这需要一个带类型参数的关联类型 `Of<B>`，加一个 `Inner` 记录当前元素类型：

```rust
trait Functor {
    type Inner;
    type Of<B>;
    fn fmap<B>(self, f: impl FnMut(Self::Inner) -> B) -> Self::Of<B>;
}
impl<A> Functor for Option<A> {
    type Inner = A; type Of<B> = Option<B>;
    fn fmap<B>(self, f: impl FnMut(A) -> B) -> Option<B> { self.map(f) }
}
// Vec<A> is implemented the same way: Of<B> = Vec<B>, via into_iter().map(f).collect()
```

使用方只写一份：

```rust
fn label<F: Functor<Inner = i32>>(c: F) -> F::Of<String> { c.fmap(|n| format!("#{n}")) }
// label(Some(3))      -> Some("#3")
// label(vec![1, 2])   -> ["#1", "#2"]
```

`label` 对任何元素是 `i32` 的函子容器成立，返回同形状但元素是 `String` 的容器。这就是 HKT 的核心收益：抽象的是「容器」，而不是某个具体容器。

但笨重之处很明显：

1. **约束要拆成两部分写**：`Inner` 描述当前元素，`Of<B>` 描述变换后的容器，调用者要写 `Functor<Inner = i32>`，而 Haskell 只需要 `Functor f => f Int -> f String`。
2. **不能对已有的类型构造器直接说话**：`Option` 和 `Vec` 都要手写一遍这个 trait 才有效，标准库本身不提供，所以第三方库各定义一套，互不通用。
3. **类型推导吃力**：嵌套多层 `F::Of<G::Of<B>>` 时，错误信息难读。
4. **更高层的抽象（Monad、`traverse`）要求更多这类编码**，复杂度快速上升。

所以多数 Rust 代码并不使用它：同样的目的有更朴素的工具——迭代器适配器（`map`、`filter`、`collect`）和 `?` 运算符，在实践里解决了绝大多数「对不同容器写同一份逻辑」的需求。

要记住：GAT 让 HKT 的**能力**在 Rust 里成为可能，不是让它成为**好用的惯用法**。
