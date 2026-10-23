---
id: hl-hc06-cpp-ub-list
node: problems.hc06-cpu-register-bitwise
type: qa
step: 17
---
## Q
C++ 位运算题的未定义行为（UB）清单是什么？寄存器应该怎么选类型？

## A
| 写法 | 结果 |
|---|---|
| 有符号整数溢出（`INT_MAX + 1`） | UB |
| 移位位数 ≥ 类型宽度（`uint32_t` 的 `x << 32`） | **UB**（Java 是 mod 32；硬件是 0） |
| 移位位数为负 | UB |
| 无符号加减乘溢出 | 定义良好，按 2³² 回绕 |
| `__builtin_ctz(0)` / `__builtin_clz(0)` | UB |
| `std::countr_zero(0u)` / `std::countl_zero(0u)` | 定义良好，都是 32 |
| `std::toupper(c)` / `std::isspace(c)` 传负数 `char` | UB（字节 ≥ 0x80） |

选型：**寄存器用 `std::uint32_t`**（确定 32 位的无符号类型，回绕有定义，右移是逻辑的），每个移位位数显式处理，字符分类自己写 ASCII 版。

其他陷阱：用 `int` 当寄存器 → `>>` 补符号位、`1 << 31` 变负；手写旋转 `s == 0` 时右移 32 位；`static_cast<uint32_t>(initial)` 前不检查范围（`-1` 变 `0xFFFFFFFF`）；`from_chars` 不检查结束指针（`12abc` 被当 12）；`0x` 前缀留给 `from_chars`（它不认，`0xFF` 解析成 0 就停）；十进制 `010` 当八进制；十六进制输出忘补零 / 用小写。

C++ 追问：`uint32_t` vs `unsigned int`：后者宽度由平台决定；大小端对 `BSWAP` 无关，与把寄存器写进字节缓冲区有关（`memcpy` + `std::endian`）；`COMPRESS` 循环写 `m &= m - 1`，`m - 1` 把最低位的 1 变 0、其下的 0 变 1，AND 后恰好清掉最低位的 1。
