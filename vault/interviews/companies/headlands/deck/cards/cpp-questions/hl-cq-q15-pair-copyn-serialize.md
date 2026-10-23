---
id: hl-cq-q15-pair-copyn-serialize
node: cpp-questions.c-memory-ownership
type: qa
step: 28
---
## Q
三个追问：为什么 `std::pair<int,int>` 不是 trivially copyable？`std::copy`、`copy_n`、`std::ranges::copy` 的区别？把结构体序列化到网络上能直接 `memcpy` 吗？

## A
- **`pair<int,int>`**：它的赋值运算符是用户提供的（user-provided），所以不满足 trivially copyable，哪怕只装两个 `int`。
- **三个 copy**：`copy_n` 是按个数的版本；`std::ranges::copy` 接收一个范围，并返回两个迭代器。
- **序列化**：不要对结构体盲目 `memcpy`——填充（padding）、字节序（endianness）和布局各平台不同；要逐字段写出，或使用固定布局的紧凑消息。
