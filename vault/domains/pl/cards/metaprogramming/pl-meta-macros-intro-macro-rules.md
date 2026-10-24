---
id: pl-meta-macros-intro-macro-rules
node: metaprogramming.macros
type: qa
step: 3
---
## Q
Rust 的 `macro_rules!` 是什么？它按什么方式匹配和展开，一个小例子里发生了什么？

## A
**是什么**：`macro_rules!` 是 Rust 内置的声明式宏（declarative macro）。你写一组「模式 → 展开结果」的规则，编译器在解析源码后，遇到 `名字!(...)` 就按模式匹配括号里的 token，匹配上就用对应的模板生成代码，替换回原处。调用时名字后面的 `!` 是警告标记：这不是函数。

**心智模型**：这是一个带模式匹配的代码模板。模式里的 `$x:expr` 表示「在这里匹配一个表达式，叫它 `$x`」；`$( ... ),*` 表示括起来的部分重复任意多次，用逗号分隔；展开模板里也用同样的重复语法。

**场景**：实现一个类似 `vec![]` 的宏，接受任意多个元素：

```rust
macro_rules! my_vec {
    ( $( $x:expr ),* ) => {{
        let mut v = Vec::new();
        $( v.push($x); )*
        v
    }};
}
let a = my_vec![1, 2, 3];   // expands to three push calls
```

调用 `my_vec![1, 2, 3]` 得到 `[1, 2, 3]`，`my_vec![]` 得到空向量。函数做不到这点，因为 Rust 函数的参数个数在定义时固定。

**要记住的一点**：展开发生在编译期、类型检查之前，展开结果必须是合法的 Rust；`$x:expr` 匹配到的是一个已经解析好的表达式整体，不是文本，所以不会出现 C 宏的优先级问题。标准库的 `println!`、`vec!`、`assert_eq!` 都是这样的宏。
