---
id: pl-abstraction-higher-kinded-foundation-gat
node: abstraction.higher-kinded
type: qa
step: 4
---
## Q
Rust 的泛型关联类型（GAT）是什么？它解决了普通 `Iterator` 做不到的什么事，并且为什么被说成是「部分的 HKT」？

## A
普通的关联类型是一个固定的类型，比如 `Iterator::Item`。**泛型关联类型**（generic associated type，GAT，Rust 1.65 稳定）让关联类型自己带参数，参数可以是**生命周期**或**类型**：`type Item<'a>`、`type Of<B>`。

它首先解决的是生命周期问题：**借用迭代器自身缓冲区的元素**。标准 `Iterator` 的 `next` 返回的元素生命周期与迭代器本身无关，所以无法返回指向迭代器内部的借用。试着实现一个返回可变窗口的迭代器：

```rust
impl<'t> Iterator for W<'t> {
    type Item = &'t mut [i32];
    fn next(&mut self) -> Option<&'t mut [i32]> {
        let r = self.data.get_mut(self.start..self.start + 2)?;
        self.start += 1;
        Some(r)
    }
}
```

```console
error: lifetime may not live long enough
  method was supposed to return data with lifetime `'t` but it is returning data with lifetime `'1`
```

因为重叠的窗口会让两次 `next` 返回的可变借用互相别名，`Iterator` 的签名不允许这样。用 GAT 写一个**借出型迭代器**（lending iterator），元素的生命周期绑定在每次对 `next` 的借用上：

```rust
trait LendingIter {
    type Item<'a> where Self: 'a;
    fn next<'a>(&'a mut self) -> Option<Self::Item<'a>>;
}
```

用重叠窗口求前缀和，`[1, 2, 3, 4]` 逐个窗口 `win[1] += win[0]`，得到 `[1, 3, 6, 10]`。

为什么是「部分 HKT」：`type Of<B>` 这种带**类型参数**的关联类型，本质上就是一个类型构造器，可以用来编码出 `Functor`：让 trait 的实现者同时声明「换掉元素类型后的同类容器是什么」。但它是借 trait 的关联类型迂回表达，不是真正地对类型构造器抽象，所以写起来笨重。

在 Java、Go、Python 里，没有对应物：它们靠垃圾回收，不存在「返回值借用自身缓冲区」的限制，所以这个问题不会出现。
