---
id: pl-types-null-safety-mechanism
node: types.null-safety
type: qa
step: 6
---
## Q
空指针异常在机器层面是怎么发生的？Rust 的 `Option<Box<T>>` 为什么不比普通指针占更多空间？

## A
`null` 在底层就是地址 0。解引用它时，操作系统的内存保护触发段错误（segmentation fault）：Go 的运行时把这个信号转成 `panic: runtime error: invalid memory address or nil pointer dereference`；JVM 捕获同一信号并抛出 `NullPointerException`。Java 14 起的「有帮助的异常信息」会指出具体是哪个表达式为空，例如 `Cannot invoke "String.length()" because "s" is null`。

`Option<T>` 是普通的枚举：`None` 或 `Some(T)`。通常带一个标记位，所以 `Option<i32>` 占 8 字节（4 字节值加对齐后的标记），比 `i32` 的 4 字节大。但对「永远非空」的指针类类型，Rust 做了空指针优化（null pointer optimization）：用地址 0 表示 `None`，其余地址表示 `Some`。实际测量：

```console
8 8 4 8
```

四个数依次是 `Box<i32>`、`Option<Box<i32>>`、`i32`、`Option<i32>` 的字节数（`std::mem::size_of`）。`Option<Box<i32>>` 和 `Box<i32>` 同样是 8 字节，没有任何额外开销。也就是说，Rust 的做法在机器码层面和 C 的「检查指针是否为 0」一样，只是检查被编译器强制了，类型系统保证不会忘记。

Go 的另一半设计：很多 `nil` 是可用的。`nil` 切片长度为 0 且能 `append`，从 `nil` map 读取返回零值，只有写入才 panic。这是「零值可用」哲学让 `nil` 在多数场景里无害。
