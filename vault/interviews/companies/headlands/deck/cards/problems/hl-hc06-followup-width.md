---
id: hl-hc06-followup-width
node: problems.hc06-cpu-register-bitwise
type: qa
step: 16
---
## Q
追问：寄存器改成 64 位或可变位宽怎么办？扩展成 8 个寄存器 `R0..R7` 怎么设计？

## A
**64 位**：`long` + `Long.*Unsigned`（`Long.toUnsignedString`、`Long.compareUnsigned`）；所有 `Integer.*` 换 `Long.*`。**可变位宽 w**：每次运算后 `& ((1L << w) - 1)`；w == 64 时 `1L << 64 == 1`（mod 64）要特判。

C++：把 `Reg` 换成 `uint64_t`，所有 32 换成 64（用 `std::numeric_limits<Reg>::digits`，不要散落字面量），`0xFFFFFFFF` 换成 `~Reg{0}`；`from_chars` 的范围检查改成「`from_chars` 本身溢出就是 `out_of_range`」。

**8 个寄存器**：加一层 `Operand`（`Reg(int index)` 或 `Imm(int value)`），寄存器文件用 `int[8]`；指令如 `AND R3 0xFF`。性能版本里 `args` 变成两个数组（目标寄存器 + 操作数 / 源寄存器），热循环 `regs[dst] = regs[dst] & (isImm ? imm : regs[src])`；把「立即数还是寄存器」也在解码时分成不同操作码，避免循环里再判断。

相关变体：同一个模拟器对 `uint64_t` 寄存器再做一遍；位集（bitset）、位板（bitboard）、flag 枚举——同一套技巧换个包装。C++：`std::bitset<N>`、`uint64_t` 位板（棋盘 64 格）。

「Java 没有 unsigned int 怎么办」的口述：「32 个 bit 一样，只是怎么读不同。我用 int 存，在三处显式用无符号版本：右移、转 long、打印。」
