---
id: pl-memory-lifetimes-pitfall-static
node: memory.lifetimes
type: qa
step: 6
---
## Q
Rust 的 `'static` 是什么意思？为什么说它不等于「永远活着」，常见的误用是什么？

## A
`'static` 是最长的生命周期，表示「这个引用可以在整个程序运行期间有效」。有两类取值：
1. 字面量：`"hello"` 的类型是 `&'static str`，数据放在二进制的只读段里。
2. 被刻意泄漏的堆数据：`Box::leak(Box::new(vec![1]))` 返回 `&'static mut Vec<i32>`，永远不会被释放。

容易混淆的是**泛型约束** `T: 'static`。它的意思是「`T` 里不含任何非静态的借用」，包括拥有数据的类型。所以 `String` 满足 `'static`，而 `&String`（借用了局部变量）不满足：

```rust
fn needs_static<T: 'static>(_t: T) {}
needs_static(String::from("x"));   // ok: owns its data
let s = String::from("y");
needs_static(&s);                  // borrowed local
```

```console
error[E0597]: `s` does not live long enough
  argument requires that `s` is borrowed for `'static`
```

这就是 `thread::spawn` 要求闭包是 `'static` 的原因：新线程可能比当前函数活得更久，不能带着对局部变量的借用。

常见误用：
1. 编译器抱怨生命周期，就把所有地方都改成 `'static`，或者用 `Box::leak` 糊弄。泄漏换来了编译通过，内存却再也回不来。
2. 把「值是 `'static` 约束」理解成「值永不被释放」：`String` 照样会 `drop`。

正确的思路：先问数据归谁。需要跨线程或存很久，就交出所有权（克隆、`Arc`），而不是延长借用。
