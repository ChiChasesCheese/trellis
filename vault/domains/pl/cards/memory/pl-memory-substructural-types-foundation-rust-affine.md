---
id: pl-memory-substructural-types-foundation-rust-affine
node: memory.substructural-types
type: qa
step: 2
---
## Q
Rust 的类型为什么是仿射而不是线性的？不使用一个值会怎样，`mem::forget` 又说明了什么？

## A
Rust 里一个值的所有者唯一：移动之后原变量不可再用，这就是「至多一次」。

```rust
let f = File::open("mv.rs").unwrap();
let g = f;                  // move: f is no longer usable
drop(g);
f.read_to_string(&mut s);   // error[E0382]: borrow of moved value: `f`
```

编译器还给出了提示：`you can use File::try_clone to duplicate a File instance`，即复制必须是显式的操作，而且复制出的是一个新的资源（新的文件描述符）。

但 Rust **不要求你使用**每个值。变量不用只会得到一个警告，离开作用域时由 `Drop` 自动清理：

```rust
// Token's Drop impl prints "drop <name>"
let a = Token("a");          // never used again
let b = Token("b");
std::mem::forget(b);         // safe code, leaks b
println!("end of main");
```

输出 `end of main` 然后 `drop a`，而 `drop b` **从未出现**：`a` 被自动销毁，`b` 因为被 `forget` 而永远泄漏。

这说明两点：

1. **Rust 是仿射的**：值可以被丢弃（弱化律成立），所以「必须用掉」并不是语言规则。线性类型才要求每个值都被显式消耗。
2. **泄漏在安全 Rust 里是允许的**：`mem::forget` 是安全函数，`Rc` 循环引用也会泄漏。Rust 的安全保证不包含「析构一定会运行」，包含的是「不会出现内存不安全」。

历史上这是个重要的决定：Rust 1.0 之前曾有一个依靠 `Drop` 保证线程不越过作用域的 API（`thread::scoped`），发现 `mem::forget` 能让析构不执行，从而导致悬空引用，该 API 被移除，转而确认「泄漏是安全的」，并在后来用闭包式的 `thread::scope` 提供安全的版本。

要记住的事实：仿射给你「不会重复释放」，不给你「一定会释放」。需要后者的协议，要用别的办法，比如把清理放进闭包，或用类型状态让错误用法不能编译。
