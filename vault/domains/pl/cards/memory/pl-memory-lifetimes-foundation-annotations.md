---
id: pl-memory-lifetimes-foundation-annotations
node: memory.lifetimes
type: qa
step: 3
---
## Q
生命周期标注 `'a` 是什么意思？什么时候必须写，`'static` 又是什么？

## A
大多数情况下编译器自己推导生命周期，不用写。必须写的场合：函数有多个引用参数，返回值又借用了其中一个，编译器无法知道是哪一个。

```rust
fn longest(a: &str, b: &str) -> &str { if a.len() >= b.len() { a } else { b } }
```

```console
error[E0106]: missing lifetime specifier
  the signature does not say whether it is borrowed from `a` or `b`
```

修复是加上生命周期标注 `'a`（一个区域的名字，读作“tick a”）：

```rust
fn longest<'a>(a: &'a str, b: &'a str) -> &'a str { ... }
```

意思是：`a`、`b` 和返回值在同一个区域 `'a` 里有效；调用时 `'a` 取实参有效期的**交集**（较短的那个）。标注**不改变任何值的寿命**，只是描述参数与返回值的关系，让编译器能在不看函数体的情况下检查调用方。

**省略规则**让常见情形不用写：只有一个输入引用时，输出就用它；有 `&self` 的方法，输出用 `self` 的生命周期。

**`'static`** 是最长的生命周期，表示“整个程序运行期间有效”。字符串字面量 `"hello"` 就是 `&'static str`（数据放在可执行文件里）。

结构体存引用也要标注：`struct Parser<'a> { input: &'a str }` 表示 `Parser` 不能比它借用的那段文本活得更久。

要记住的一个事实：生命周期标注是写给编译器的“引用关系说明书”，写不出来通常说明数据流本身需要重新设计。
