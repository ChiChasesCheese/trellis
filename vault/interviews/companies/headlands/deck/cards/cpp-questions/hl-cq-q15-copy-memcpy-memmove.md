---
id: hl-cq-q15-copy-memcpy-memmove
node: cpp-questions.c-memory-ownership
type: qa
step: 26
---
## Q
面试题：`std::copy`、`memcpy` 和 `memmove` 有什么区别？
What's the difference between `std::copy`, `memcpy` and `memmove`?

## A
- **`memcpy` / `memmove`**：复制**原始字节**，只对 trivially copyable 的类型安全。`memcpy` 的两块内存**不能重叠**（重叠是未定义行为），`memmove` 可以重叠。
- **`std::copy`**：类型感知，对每个元素调用赋值运算符，适用任意迭代器。
- 对 trivially copyable 的类型，标准库会把 `std::copy` 自动退化成 `memmove`——所以用 `std::copy` **又安全又不慢**。实测对 `int` 数组 `-O2 -S`，汇编就是一次 `bl _memmove`。
- 类型双关（type punning）用 `std::bit_cast`，不用指针强转。
