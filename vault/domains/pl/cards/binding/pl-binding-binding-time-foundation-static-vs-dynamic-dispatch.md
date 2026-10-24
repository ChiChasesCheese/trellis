---
id: pl-binding-binding-time-foundation-static-vs-dynamic-dispatch
node: binding.binding-time
type: qa
step: 4
---
## Q
同样是「调用某个类型的方法」，Rust 的泛型和 `dyn Trait` 在绑定时机上差在哪里？这个差别在内存里是什么样的？

## A
调用 `x.speak()` 时，编译器是否知道 `x` 的具体类型，决定了绑定在编译时还是运行时。Rust 让你在两种之间显式选择：

```rust
fn stat<T: Speak>(t: &T) -> &'static str { t.speak() }   // bound at compile time
fn dynm(t: &dyn Speak) -> &'static str { t.speak() }     // bound at run time
```

**泛型**（`T: Speak`）：编译器对每个用到的具体类型各生成一份函数副本（单态化，monomorphization），`speak` 的调用在副本里是对一个已知函数的直接调用，可以被内联。代价是代码体积随类型数量增长。

**`dyn Speak`**（trait 对象）：只有一份代码，调用时通过对象携带的函数表（虚表，vtable）找到真实实现。所以引用必须变成**胖指针**：一个指向数据，一个指向虚表。

```rust
println!("{} {}",
    std::mem::size_of::<&Dog>(),          // 8
    std::mem::size_of::<&dyn Speak>());   // 16
```

输出 `8 16`：引用体积翻倍，每次调用多一次间接跳转，而且编译器看不到被调用的函数，内联不了。

C++ 的两个选项与此一一对应：模板对应泛型的单态化，`virtual` 函数对应 `dyn Trait`。区别在虚表指针放在哪里：Rust 把它放在引用上（胖指针），C++ 把它藏在对象里面（每个对象多一个隐藏指针）。
```cpp
struct Plain { int x; };
struct Virt  { int x; virtual int f() const { return x; } };
// sizeof(Plain) = 4, sizeof(Virt) = 16   (8-byte vptr + 4 + padding)
```
本机实测输出 `4 16`：同样一个 `int` 字段，有虚函数的对象大了三倍，多出来的是虚表指针和对齐填充，所以含虚函数的类不能再按 4 字节摆在数组里。
Java 的做法是默认走「运行时查表」：普通方法调用（`invokevirtual`、`invokeinterface`）都按对象的真实类型找实现，只有 `private`、`static`、`final` 方法能在编译时定死。Go 的接口调用同样按「类型指针 + 函数表」查，具体类型的调用则是直接调用。

结论：同一语义可以用不同绑定时机实现，性能与灵活性的天平由程序员在类型层面选择（Rust、Go），或由运行时事后修正（Java）。
