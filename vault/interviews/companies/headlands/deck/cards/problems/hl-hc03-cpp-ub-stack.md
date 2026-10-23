---
id: hl-hc03-cpp-ub-stack
node: problems.hc03-recursive-sum
type: qa
step: 22
---
## Q
C++ 版递归求和的核心陷阱有哪些？`INT_MAX + 1` 与 `UINT_MAX + 1` 分别是什么，`-O0` 和 `-O2` 对尾递归的差别是什么？

## A
1. **有符号溢出是 UB**，不是回绕：`INT_MAX + 1` 未定义（可能回绕成负数，也可能被优化器利用）；`UINT_MAX + 1` 是定义良好的回绕，结果 0。`-fsanitize=undefined` 能抓到；想要回绕就用无符号类型。
2. **指望尾调用消除**：`-O0` 下 `sum_tail` 与普通递归都会栈溢出崩溃，`[[clang::musttail]]` 强制尾调用则不会；`-O2` 下三种都通过。标准不保证任何一种。
3. **栈溢出当成可捕获的错误**：它是信号（`SIGSEGV`），不是异常；`sum_recursive(1'000'000, Width::Long)` 在 512 KiB 栈上直接崩，不能 `try/catch`。
4. `n * (n + 1) / 2` 先乘后除；先把偶数因子除 2，或用 `__int128`。
5. **用 `double` 并行求和**：浮点加法不满足结合律。
6. **`std::execution::par`**：`std::reduce(std::execution::par, …)` 在 libstdc++ 里依赖 TBB，在 libc++ 里还是实验性的；面试里说「标准有这个接口，但可用性取决于标准库实现」，然后手写 `std::async` / `std::thread` 版。
7. **`Trampoline` 的构造函数不能写成可变参数模板 `Trampoline(A&&...)`**：对非 const 左值 `Trampoline t2 = t1;`，`A&&`（`A = Trampoline&`）比 `const Trampoline&` 的拷贝构造更匹配，被选中后去构造 `variant` 而编译失败；用带标签的构造函数避免。
