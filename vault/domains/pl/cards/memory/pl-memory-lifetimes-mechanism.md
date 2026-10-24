---
id: pl-memory-lifetimes-mechanism
node: memory.lifetimes
type: qa
step: 4
---
## Q
Rust 的生命周期标注 `'a` 到底标注了什么？编译器怎样用它检查调用？

## A
`'a` 是一个区域的名字，代表程序里的一段区间。关键事实：**标注不会改变任何值的寿命**，它只是在函数签名里描述「输入引用和输出引用之间的关系」，让编译器在不看函数体的前提下检查调用。

```rust
fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {
    if a.len() >= b.len() { a } else { b }
}
```

签名的意思是：返回的引用在 `'a` 内有效，而 `'a` 同时被 `a` 和 `b` 的有效期包住。函数体里返回的是 `a` 或 `b`，编译器就能验证这个承诺。

调用处的求解过程：`longest(&a, &b)` 里，`a` 的借用活到 `main` 结束，`b` 的借用只活到内层花括号结束，`'a` 取两者的**交集**，即较短的那个。于是返回值最多只在 `b` 还活着的区间内可用。

```rust
{
    let b = String::from("hi");
    res = longest(&a, &b);
}                                  // b dropped here
println!("{}", res);               // error: `b` does not live long enough
```

如果结果在 `b` 销毁之后使用，编译器报 `E0597`。

有三条省略规则（elision）让多数函数不用写标注：
1. 每个引用参数各得一个独立的生命周期。
2. 只有一个输入生命周期时，输出就用它。
3. 有 `&self` 或 `&mut self` 时，输出用 `self` 的生命周期。

这些检查全在编译期完成，生成的代码里没有生命周期的任何痕迹。
