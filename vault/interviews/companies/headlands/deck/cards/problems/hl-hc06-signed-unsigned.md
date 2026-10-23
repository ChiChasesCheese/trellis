---
id: hl-hc06-signed-unsigned
node: problems.hc06-cpu-register-bitwise
type: qa
step: 3
---
## Q
同样 32 个 bit，有符号和无符号读法有什么区别？Java 没有无符号 int，应该怎么处理寄存器？

## A
补码（two's complement）：最高位（第 31 位）权重是负的 −2³¹，其余照旧。8 位例：`1111 1111` 有符号读 −1、无符号读 255；`1000 0000` 有符号 −128、无符号 128；`0111 1111` 两种读法相同（最高位为 0）。32 位同理：`0xFFFFFFFF` 有符号 **−1**，无符号 **4 294 967 295**；`0x80000000` 有符号 −2 147 483 648，无符号 2 147 483 648。

**Java 做法**：用 `int` 存位模式（bit 一样，只是解释不同）。位运算 `& | ^ ~ <<` 只看 bit，无区别；只有三类操作结果不同，必须显式选无符号版本：
- **右移** 用 `>>>`（逻辑，补 0），不用 `>>`（算术，补符号位）；
- **转 long** 用 `Integer.toUnsignedLong(reg)`（零扩展），`(long) reg` 是错的（符号扩展成 `-1L`）；
- **打印** 用 `Integer.toUnsignedString(reg)`；**比较** 用 `Integer.compareUnsigned`。
64 位寄存器对应 `Long.*Unsigned`。

```java
int reg = 0xFFFFFFFF;                        // 值是 -1
long u = Integer.toUnsignedLong(reg);        // 4294967295L
Integer.compareUnsigned(0x80000000, 1) > 0;  // true
```
C++ 做法：`std::uint32_t`（宽度确定为 32 位的真无符号类型，回绕有定义，右移是逻辑的）；`unsigned int` 的宽度由平台决定，标准只保证 ≥ 16。
