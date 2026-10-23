---
id: hl-hc06-rotate
node: problems.hc06-cpu-register-bitwise
type: qa
step: 6
---
## Q
循环移位（rotate）和普通移位有什么区别？手写旋转有哪些坑，库函数怎么用？

## A
旋转：挪出去的 bit 从另一头**绕回来**，一个不丢。`x = 0x12345678`：`ROL 4` = `0x23456781`（最高 4 位 `0001` 绕到最低位）；`ROR 4` = `0x81234567`。位数对 32 取模：`ROL 32` 不变，`ROL 36 == ROL 4`，`ROL 0` 不变。

库函数：`Integer.rotateLeft(x, n)` / `rotateRight` 已按 `n mod 32` 处理（`Rol(Integer.MAX_VALUE)` 也安全），是 JIT intrinsic，编译成一条旋转指令。C++20：`std::rotl` / `std::rotr`（`<bit>`），对任意位数定义良好。

手写的坑：`(x << n) | (x >>> (32 - n))` 在 `n == 0` 时 `x >>> 32 == x`，碰巧正确；换成 `>>` 就错（符号扩展污染）；C++ 里 `(x << s) | (x >> (32 - s))` 在 `s == 0` 时右移 32 位是 UB。C++ 无 UB 的惯用形式：`(x << (s & 31)) | (x >> (-s & 31))`，主流编译器能识别成旋转指令。

测试：`ROL 36` 与 `ROL 4` 必须相同。
