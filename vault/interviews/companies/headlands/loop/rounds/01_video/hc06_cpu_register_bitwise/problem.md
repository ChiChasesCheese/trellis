# hc06 · CPU 寄存器位运算

一个 CPU 寄存器就是 32 个开关（bit）。你拿到它的初值和一串指令（与、或、异或、取反、移位……），依次执行，输出最后的值。代码本身很短，分数在细节上：Java 没有无符号 `int`，移位 32 位及以上在 Java 和 C++ 里都不是你想的那样，循环移位的位数为 0 时容易写出未定义行为。题目是一个函数 `solve(lines) → 输出行`，Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "You have a 32-bit unsigned register. Read its initial value, then apply a list of operations: AND, OR, XOR, NOT, shift left, shift right. Print the final value. If the input is malformed, print 'Malformed Input'."
> 接着会问："What happens if you shift by 32?" "Now add rotate left and right." "Print it in hex and in binary." "What if the register were 64 bits?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：数是十进制吗？指令大小写？移位位数超过 31 怎么算？ |
| 3–15 分钟 | **Part 1**：与、或、异或、取反、移位，十进制输出 |
| 15–30 分钟 | **Part 2**：循环移位，输出格式 |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 六条指令（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static List<String> solve(List<String> lines)` |
| C++ | `std::vector<std::string> solve(const std::vector<std::string>& lines)` |

- 第一行是寄存器初值，十进制，范围 `0..4294967295`。之后每行一条指令，指令名全大写，用空格隔开参数：`AND x` · `OR x` · `XOR x` · `NOT`（没有参数）· `SHL k` · `SHR k`。
- `x` 和 `k` 都是十进制，范围 `0..4294967295`。`SHL` / `SHR` 是逻辑移位（补 0）；`k >= 32` 时结果是 0。
- 返回一行：终值的十进制。例子：`["240", "AND 60", "SHL 4", "OR 15"]` → `["783"]`（`240 & 60 = 48`，`48 << 4 = 768`，`768 | 15 = 783`）。
- 任何错误（空输入、初值或参数不是十进制数或超出范围、未知指令、参数个数不对、小写指令名、空行）→ 只返回 `["Malformed Input"]`。

## Part 2 · 循环移位和输出格式（约 15 分钟）

函数不变，增加两件事：

- `ROL k` · `ROR k`：循环左移 / 右移，被挤出去的位从另一头绕回来；位数对 32 取模，所以 `ROL 0`、`ROL 32` 都不改变寄存器，`ROL 36` 等于 `ROL 4`。例子：`0x12345678`（305419896）`ROL 4` 得 `0x23456781`（591751041）；`0x80000001`（2147483649）`ROL 1` 得 3。
- 最后一行可以是输出格式 `DEC` / `HEX` / `BIN`（不写就是 `DEC`）。`HEX` 输出 `0x` 加 8 位大写十六进制，如 `0x000000FF`；`BIN` 输出 32 位二进制，如 `00000000000000000000000000000101`。格式只能出现在最后一行，写在中间算未知指令。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. Java 没有无符号 `int`，你怎么表示这个寄存器？
2. 为什么 `SHL 32` 要单独处理？
3. `>>` 和 `>>>` 有什么区别？这里该用哪个？
4. 循环移位怎么写才不会出错？`ROL 0` 为什么是陷阱？
5. 如果寄存器是 64 位，哪些地方要改？
6. 为什么不能用 `Integer.parseInt` 解析操作数？

## 边界

- 寄存器最高位为 1（`NOT` 之后、`4294967295`）时的 `SHR`、输出
- `SHL 0` / `SHL 31` / `SHL 32` / `SHR 33` / `SHL 4294967295`
- `ROL 0` / `ROL 32` / `ROL 36`
- 初值 `0`、`4294967295`、`4294967296`（非法）、`-1`、`+5`（非法）
- `AND 4294967295`（`Integer.parseInt` 会抛异常）
- 空输入、空行、`NOT 2`、`AND` 缺参数、小写指令名

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc06_cpu_register_bitwise       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc06_cpu_register_bitwise --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc06_cpu_register_bitwise       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc06_cpu_register_bitwise --tag part1
```
