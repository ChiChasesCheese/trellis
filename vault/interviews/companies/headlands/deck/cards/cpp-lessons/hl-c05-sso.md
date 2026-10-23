---
id: hl-c05-sso
node: cpp-lessons.c05-stl-containers
type: qa
step: 8
---
## Q
面试问：`std::string` 的小字符串优化（SSO，small string optimization）是什么？
Interview question: What is the small string optimization?

## A
- `std::string` 本身是连续字符块；**短字符串直接存在 `string` 对象内部的缓冲区里**，省掉一次堆分配。
- 实测（libc++）：`sizeof(std::string)` = 24，空串容量 22；长度 5、22 的字符串在对象内部（无分配），长度 23、40 的在**堆**上。
- 阈值依标准库实现而不同（GCC 是 15）。
- `string` 移动后源对象是否为空，取决于字符是否存放在 SSO 缓冲区内。
