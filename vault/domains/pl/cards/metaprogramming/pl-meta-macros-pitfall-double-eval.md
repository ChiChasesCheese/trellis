---
id: pl-meta-macros-pitfall-double-eval
node: metaprogramming.macros
type: qa
step: 10
---
## Q
C 宏经典的两个坑（优先级、重复求值）是什么？Rust 的 `macro_rules!` 解决了哪个，哪个仍然存在？

## A
```c
#define SQUARE(x) x*x
#define MAX(a,b) ((a)>(b)?(a):(b))
// SQUARE(1+2)    -> 1+2*1+2 = 5, not 9
// MAX(next(), 0) -> next() is called twice
```

真实输出：`SQUARE(1+2)=5`；`MAX(next(),0)=2, next called 2 times`。原因：C 宏是纯文本替换，参数 `1+2` 被原样粘进 `x*x`，运算符优先级把它拆开；参数 `next()` 在展开后出现两次，所以被执行两次。

Rust 的同类写法：

```rust
macro_rules! square { ($x:expr) => { $x * $x }; }
// square!(1 + 2)  -> 9
// square!(next()) -> next called 2 times
```

真实输出：`square!(1+2)=9`；`square!(next())=2 next called 2 times`。

**结论**：优先级问题被解决了，因为 `$x:expr` 展开的是一个已解析的整体表达式。重复求值问题仍在，因为宏展开仍然是在语法层面复制参数。写法是在宏里先 `let v = $x;` 再用 `v * v`。这提醒我们：宏的参数不是值，是代码，代码每出现一次就执行一次。这也是为什么「看起来像函数调用」的宏（`square!(x)`）比真函数更危险，Rust 用 `!` 后缀强迫你看见它是宏。

C++ 的现代修法是不用宏：`std::max(next(), 0)` 是真函数，参数只求值一次，实测输出 `max=1 next called 1 times`，并且有类型检查。C 的 `MAX` 宏在 C++ 里已经没有存在的理由。
