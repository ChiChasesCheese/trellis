---
id: pl-memory-memory-safety-foundation-bounds-ub
node: memory.memory-safety
type: qa
step: 2
---
## Q
边界检查（bounds check）和未定义行为（undefined behavior）是什么？同一个越界访问，C、C++ 与 Go、Rust、Java、Python 的结果有何不同？

## A
数组或切片在运行时带着长度。**边界检查**就是每次 `v[i]` 之前先比较 `i` 与长度：`i >= len` 就进入语言定义的错误路径，否则才读写内存。成本是一次比较和一个几乎总被预测正确的分支，现代 CPU 上很小，编译器常常还能证明下标安全而把检查删掉。

**未定义行为**（UB）是 C/C++ 标准的术语：违反规则（越界读写、释放后使用）时，标准不规定结果，编译器甚至可以假设它不会发生并据此优化；实际可能崩溃、可能读到别处的数据、也可能被攻击者利用来执行任意代码。

同样是读一个 3 个元素数组的第 5 个元素：

```console
C         打印出 1：没有任何报错，读到相邻内存的垃圾值（实测）
C++       v[5] 打印出 1，同样没有报错（实测）；v.at(5) 抛 std::out_of_range
Go        panic: runtime error: index out of range [5] with length 3
Rust      panicked: index out of bounds: the len is 3 but the index is 5
Java      ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 3
Python    IndexError: list index out of range
```

四种安全语言都在运行期拦下来，程序以明确的错误终止（或被捕获）；C 只有一个地址，没有长度，什么都不检查。C++ 的 `std::vector` 带着长度，却默认不检查 `operator[]`（`at()` 才检查），行为与 C 相同。用 AddressSanitizer 编译才会看到 `heap-buffer-overflow`；用 libc++ 的加固模式（`-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST`）编译，`v[5]` 会变成立即终止的陷阱（本机退出码 133），代价是每次访问多一次比较，和其他语言的默认行为一样。

要记住的一个事实：内存安全的第一层是“别让一次越界变成读写任意内存”，代价是每次访问多一次比较。
