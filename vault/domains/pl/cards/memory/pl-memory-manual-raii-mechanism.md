---
id: pl-memory-manual-raii-mechanism
node: memory.manual-raii
type: qa
step: 5
---
## Q
RAII 在编译后是怎么工作的？析构（drop）的调用顺序由什么规则决定？

## A
编译器知道每个变量的作用域，于是在作用域的每一个出口插入对该变量析构函数的调用，不依赖任何运行时追踪。出口包括：执行到右花括号、`return`、`break`，以及（有异常或 panic 展开时）异常路径。

规则：
1. 局部变量按**声明顺序的逆序**析构。后创建的可能依赖先创建的，所以先拆后建的。
2. 结构体的字段按声明顺序析构，先执行结构体自己的析构代码，再析构字段。
3. 被移动走的值不在原处析构，由新的所有者负责。

一个小轨迹（Rust 的 `Drop`）：

```rust
let _a = Noisy("a");
{ let _b = Noisy("b"); println!("inner scope end"); }
let c = Noisy("c");
drop(c);                      // explicit early drop
let _d = Noisy("d");
println!("main end");
```

```console
inner scope end
drop b
drop c
main end
drop d
drop a
```

`b` 在内层右花括号处析构；`c` 在显式 `drop(c)` 处；`main` 结束时按逆序先 `d` 后 `a`。

成本：没有运行时开销，析构调用就是普通函数调用，且在编译期已确定位置。代价是生命周期必须是词法嵌套的：一个值只能活到所属作用域结束（或者被移动到另一个作用域），不能由「最后一个使用者」随时决定。
