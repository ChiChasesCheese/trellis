---
id: pl-memory-lifetimes-go-vs-rust-return
node: memory.lifetimes
type: qa
step: 6
---
## Q
同样是「返回局部变量的地址」，Go 能直接写、C 是错误、Rust 编译不过，三者的区别说明了什么？

## A
```go
func make1() *string {
	s := "x"
	return &s            // fine in Go
}
```

输出 `x`。Go 的编译器发现 `s` 的地址逃出了函数，自动把 `s` 分配在堆上，由 GC 管理，程序员不需要知道。

```rust
fn make() -> &String { let s = String::from("x"); &s }
```

```console
error[E0106]: missing lifetime specifier
  this function's return type contains a borrowed value,
  but there is no value for it to be borrowed from
```

Rust 没有 GC 可以兜底，局部变量在函数返回时一定释放，所以引用不可能活着出去。编译器要求你换一个所有权方案：返回 `String`（把所有权交出去），或者让调用者提供存储。

C 的同一个写法会编译（至多警告），运行时得到悬空指针，读到什么取决于栈上之后被谁覆盖。

三种回答，其实是同一个问题的三个答案：
- Go（和 Java、Python）：运行时系统延长值的寿命，**写法自由，成本在运行期**。
- Rust：编译期证明引用安全，**写法受限，运行期零成本**。
- C：不检查，**自由且零成本，但出错是未定义行为**。

选择一门语言，部分是在选择你愿意把「内存安全」这笔成本放在哪个阶段：运行期（GC）、编译期（借用检查）或事故发生时。
