---
id: pl-memory-stack-heap-pitfall-overflow
node: memory.stack-heap
type: qa
step: 9
---
## Q
在 Rust 与 C++ 里把一个 64 MB 的数组直接写成局部变量会发生什么？怎样改？

## A
栈很小，大块数据放在栈上会直接把栈撑破。

```rust
fn main() {
    let a = [1u8; 64 * 1024 * 1024];   // 64 MB array as a local
    println!("{}", a[a.len() - 1]);
}
```

实测结果：

```console
thread 'main' has overflowed its stack
fatal runtime error: stack overflow, aborting
```

进程以 SIGABRT 终止（退出码 134），这不是 panic，无法 `catch_unwind` 捕获。

改成堆分配即可：

```rust
fn main() {
    let a = vec![1u8; 64 * 1024 * 1024];   // buffer lives on the heap
    println!("{}", a[a.len() - 1]);         // prints 1
}
```

C++ 里同样的写法 `char a[64 * 1024 * 1024];` 也会撑破栈，但没有任何消息：本机进程直接被 SIGSEGV 终止（退出码 139），标准把它归为未定义行为（不规定后果），无法捕获。改成 `std::vector<char> a(64 * 1024 * 1024);` 即可正常运行（输出 1，退出码 0）。
同类坑还有：
- 递归没有终止条件或深度不可控，在 Java 得到 `StackOverflowError`，在 Python 得到 `RecursionError`。
- 把大数组当局部变量传值（每次调用都复制整块栈内存）。

经验：定长且不大（几 KB 以内）的数据放栈，大小不定或很大的数据放堆；递归深度取决于输入时，改写成显式栈（循环加 `Vec`）。
