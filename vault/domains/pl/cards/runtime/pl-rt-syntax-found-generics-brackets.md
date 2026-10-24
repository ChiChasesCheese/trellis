---
id: pl-rt-syntax-found-generics-brackets
node: runtime.syntax-parsing
type: qa
step: 5
---
## Q
泛型（generics）的类型参数用 `<>` 还是 `[]`？Rust 的 turbofish `::<>` 为什么存在，Java 和 Go 又怎样绕开 `<` 和 `>` 的歧义？

## A
**歧义的来源**：`<`、`>` 同时是比较运算符和泛型括号。在表达式位置，`f<A, B>(c)` 既可以读成“调用泛型函数 `f`”，也可以读成“`f < A`、`B > (c)` 两个比较”。解析器要么靠无限前瞻/回溯猜，要么靠语法强制消歧。

**Rust：turbofish**。在**类型位置**（`let x: Vec<i32>`）解析器已知道这里是类型，所以直接写 `<>`；在**表达式位置**必须写成 `::<>`，形状像一条鱼，所以叫 turbofish：
```
let n = "5".parse<i32>().unwrap();
error: comparison operators cannot be chained ... help: use `::<...>` instead
```
`"5".parse::<i32>()` 才对。换来的是：解析器永远只看一个记号就能分辨，不需要符号表；代价是一个看上去很怪的语法。

**Java：把 `<` 移到方法名之前**。`Collections.<String>emptyList()`：`.` 后面紧跟 `<` 不可能是比较，所以无歧义。`new HashMap<String, List<Integer>>()` 里 `new` 后面必定是类型。早期还有 `>>` 被词法分析器当成移位运算符的问题，解析器要把一个 `>>` 记号拆成两个 `>`。

**Go：用方括号**。`Zero[int]()` 在语法上就是“下标表达式再调用”，解析器不区分下标和实例化，留到类型检查阶段再判断 `Zero` 是函数还是切片。Go 1.18 加泛型时选 `[]` 正是为了不改变解析的简单性；它也带来类型声明里 `type T[P *C]` 要和数组类型消歧的新麻烦。

**Python**：3.12 的新语法 `def f[T](x: T)` 也用 `[]`，原因相同：`<` 在表达式里已经是比较。

规律：**新语法要寄生在已有记号上时，选择权在“让解析器猜”和“让用户多写点”之间**；Rust 选后者，Go 选了“解析器不猜，推迟到类型检查”。
