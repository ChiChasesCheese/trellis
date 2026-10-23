---
id: hl-hc03-followup-overflow-return
node: problems.hc03-recursive-sum
type: qa
step: 20
---
## Q
追问：「溢出时返回什么？为什么不抛异常？」「n = 2³²−1 时 `n*(n+1)/2` 会怎样？」两个问题怎么答？

## A
**溢出时返回什么**：输入 n 过大是调用方可能遇到的正常情况，所以是**业务结果**。用 sealed `Ok/Overflow` 迫使调用方在编译期处理，`Overflow` 带精确值（`BigInteger`）方便降级；内部为简洁抛 `ArithmeticException`，在公共入口统一转成值。热路径上抛异常很贵，但这里只抛一次。口述：「我把溢出定义成返回类型的一部分，编译器强制调用方处理。」

**`n*(n+1)/2` 在 n = 2³²−1**：乘积 2⁶⁴−2³² 在 long 里回绕成 −2³²，除 2 得 −2³¹，静默错误。解法：n 与 n+1 必有一个偶数，先除再乘，乘积只有一半；`multiplyExact`；中间量溢出时退到 `BigInteger`。

**探针**：你是凭直觉写 `n*(n+1)/2`，还是想到了乘积溢出；`multiplyExact` 抛了怎么办（`BigInteger` 兜底，而不是报溢出）；会不会自己找出 `MIN..MAX` 这类反例。

C++ 补充：怎么检测溢出——`__builtin_add_overflow`（clang/gcc）；或先用 `__int128` 加宽再判断；或加之前用 `LLONG_MAX - b` 比较。C++26 的 `std::add_sat` 是饱和运算，不会告诉你发生了溢出。
