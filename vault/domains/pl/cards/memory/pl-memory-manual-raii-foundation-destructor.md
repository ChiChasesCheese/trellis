---
id: pl-memory-manual-raii-foundation-destructor
node: memory.manual-raii
type: qa
step: 3
---
## Q
析构函数（destructor）和 Rust 的 `Drop` 是什么？RAII 的“离开作用域自动释放”是怎么发生的？

## A
**析构函数**是一段绑定在类型上的清理代码：每当这个类型的一个值**被销毁**（离开作用域、被显式丢弃），编译器就自动在那里调用它。C++ 里叫 `~Type()`，Rust 里是为类型实现 `Drop` trait（trait 即“一组方法的约定”，`Drop` 约定一个 `drop` 方法）。

RAII（Resource Acquisition Is Initialization）就是利用它：创建对象时获取资源（分配内存、打开文件），对象的析构函数里释放资源。这样“释放”不再靠程序员记得写，而是靠作用域结束这个事件触发。

```rust
struct Noisy(&'static str);
impl Drop for Noisy { fn drop(&mut self) { println!("drop {}", self.0); } }
fn main() {
    let _a = Noisy("a");
    { let _b = Noisy("b"); println!("inner end"); }
    println!("main end");
}
```

输出（一次实测）：`inner end`、`drop b`、`main end`、`drop a`。

规则：变量在其所在的花括号结束处被销毁；同一作用域里多个变量按**声明的逆序**销毁；无论函数是正常结束、提前 `return` 还是出错，销毁都会发生。

要记住的一个事实：RAII 把“资源的生命周期”绑定到“变量的作用域”，释放时机在编译期就确定，没有运行时的追踪成本。
