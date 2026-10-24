---
id: pl-memory-ownership-borrowing-mechanism
node: memory.ownership-borrowing
type: qa
step: 4
---
## Q
借用检查器（borrow checker）是怎么工作的？一个借用的有效范围到哪里为止？

## A
借用检查是编译器在类型检查之后做的一趟静态分析，对象是函数的控制流图。它为每个引用推出一段「活跃范围」：从创建引用的点，到这个引用最后一次被使用的点。然后检查在这段范围里，被借用的值有没有被冲突地使用：
- 存在 `&mut` 借用期间，不能再读写原值，也不能再借用。
- 存在 `&` 借用期间，不能修改原值，也不能 `&mut` 借用。
- 原值被移动或销毁时，不能还有活跃的借用。

关键点是「到最后一次使用为止」，而不是「到作用域结束」，这叫非词法生命周期（NLL，non-lexical lifetimes）。

```rust
let mut s = String::from("hi");
let r = &s;
println!("{}", r);   // last use of r: the borrow ends here
s.push('!');         // ok
println!("{}", s);   // hi!
```

输出 `hi` 和 `hi!`。如果在 `s.push('!')` 之后还用 `r`，才会报错。

运行时成本为零：借用、所有权、生命周期全在编译期被检查并擦除，生成的机器码和手写 C 的指针操作一样，没有任何引用计数或检查指令。代价全部落在编译时间和你的脑力上。

检查是保守的（conservative）：它拒绝一切无法证明安全的程序，所以有些其实安全的写法也会被拒绝，需要换个写法或用 `unsafe`。
