# hc06 · 思路与追问（C++20 版）

这题的代码量很小，分数都在细节：寄存器是什么类型、每个移位位数有没有处理、数字解析严不严、非法输入会不会变成 UB。C++ 没有 Java 那种「位数 mod 32」的兜底，`x << 32` 直接是未定义行为（undefined behavior，UB）。下面按 Part 写清三件事：怎么写、面试官在探什么、该说出口的那句话。完整实现和推导在讲义 [[hc06_cpu_register_bitwise_cpp]]。

## 30 秒版本

- **寄存器用 `std::uint32_t`**：宽度固定为 32，回绕有定义，`>>` 是逻辑右移。`unsigned int` 的宽度由平台决定，不能当语义用。
- **每个移位位数都显式处理**：`n >= 32` 返回 0；旋转用 `std::rotl` / `std::rotr`（任意位数都有定义）。
- **计数用 `<bit>`**：`std::popcount`、`countr_zero`、`countl_zero`，对 0 返回 32；`__builtin_ctz(0)` 是 UB。
- **解析用 `std::from_chars`**：它不认 `+`、`0x`、空白，但会在合法前缀处成功，所以必须检查结束指针；先解析到 `uint64_t` 再查范围。
- **字符分类自己写 ASCII 版**：`std::toupper` / `std::isspace` 传负的 `char` 是 UB。
- **Part 4**：解码到两个 `uint32_t` 数组，移位用 64 位做、位数夹到 ≤ 32，没有分支也没有 UB；剩下的瓶颈是 `switch` 的间接跳转。

## Part 1 · 解析与执行

**写法**：指令是小结构体，封闭集合用 `std::variant`，`apply` 用 `std::visit(overloaded{...})`，不写 `default`，新增指令时漏一个类型就编译失败。

```cpp
[&](const Shl& i) { return i.count >= 32 ? Reg{0} : Reg(r << i.count); },
[&](const Shr& i) { return i.count >= 32 ? Reg{0} : Reg(r >> i.count); },
[&](const Rol& i) { return std::rotl(r, i.count); },    // std::rotl 对任意 s >= 0 都有定义（取 mod 32）
```

`parse_value` 三步：先判断 `0x` / `0b` 前缀并去掉，再 `from_chars` 解析到 `uint64_t`，最后检查错误码、结束指针等于末尾、值 ≤ `0xFFFFFFFF`。`parse_line` 里把类型构造函数抛的 `std::invalid_argument` 翻译成 `MalformedProgram`；`MalformedProgram` 不继承 `invalid_argument`，两者不能混。`run` 的初值参数是 `long long`，先查范围再转 `Reg`。

**面试官在探什么**

1. **为什么不用 `int`**。`int` 的 `>>` 补符号位（`0xF0000000 >> 4` 得 `0xFF000000`），`1 << 31` 是 UB，打印会出负数。`uint32_t` 三个问题都没有。
2. **`x << 32` 是多少**。C++：UB，编译器可以假设它不发生；Java：位数取低 5 位，`x << 32 == x`；硬件：因指令而异。三边都不等于题目要的 0，所以必须自己判断，或者夹到 ≤ 32 后用 64 位移位。
3. **手写旋转的坑**。`(x << s) | (x >> (32 - s))` 在 `s == 0` 时右移 32 位，是 UB。无 UB 的惯用写法是 `(x << (s & 31)) | (x >> (-s & 31))`，主流编译器会把它识别成一条旋转指令；更直接的是 `std::rotl`。
4. **`static_cast<uint32_t>(-1LL)` 是 `0xFFFFFFFF`**。无符号转换按 2^32 取模、不报错，非法的初值会变成「合法」的寄存器。所以参数用 `long long`，先判断再转换。
5. **`from_chars` 的前缀陷阱**。`"12abc"` 返回成功、值是 12；`"0xFF"` 在 `x` 处停下、值是 0。不查结束指针，这些都会被悄悄接受。
6. **字符分类**。`std::toupper(c)` 的参数必须是 `unsigned char` 的值或 `EOF`；`char` 在多数平台有符号，字节 ≥ 0x80 变负数，是 UB。自己写 ASCII 版：字节 ≥ 0x80 和 NUL 都只是格式错误。
7. **`010` 是十进制 10**，不是八进制；`from_chars` 按 base 10 解析，自然满足。
8. **类型守住不变式**。`SetBit(32)` 构造不出来（构造函数抛异常），比在 `apply` 里到处检查位号可靠。

**该说出口的话**：「寄存器用 `uint32_t`，移位位数大于等于 32 在 C++ 里是 UB，所以我显式判断；解析用 `from_chars`，并且检查结束指针。」

## Part 2 · 无符号语义与输出格式

**写法**：`dec` 用 `std::to_string(Reg)`（`uint32_t` 的重载是无符号的）；`hex` 手写 8 位大写，每次取 4 位查表；`bin` 用 `std::bitset<32>(r).to_string()`（本身就补零）；`describe` 把三个拼起来。`solve`：取第一个非空非注释行作初值，其余行交给 `parse_program`，把 `MalformedProgram` 和 `invalid_argument` 转成 `{"Malformed Input"}`。只捕获这两类，不要 `catch (...)`，否则 `bad_alloc` 也会被吞成格式错误。

**面试官在探什么**

1. **怎么验证输出是对的**。往返测试：`parse_value(hex(x)) == x`，`dec` 和 `0b` + `bin` 同理。
2. **输入的脏格式**。CRLF 行尾、制表符分隔、注释行、最后一行没有换行；`getline` 读出来的行尾可能带 `\r`，解析时要当空白处理。
3. **空输入和只有注释**：没有初值，是 `Malformed Input`，不是崩溃。
4. **输出格式细节**：十六进制大写、补满 8 位；二进制补满 32 位。

**该说出口的话**：「输出前我做了往返检查：hex、dec、bin 都能解析回原值。」

## Part 3 · 扩展指令

**写法**：C++20 没有标准的 compress / expand（`std::byteswap` 是 C++23），要自己写，循环处理掩码里的每个 1：

```cpp
Reg out = 0; int k = 0;
for (Reg m = mask; m; m &= m - 1) {                 // 每次清掉最低位的 1
    const int b = std::countr_zero(m);
    out |= ((r >> b) & 1u) << k++;                  // compress：第 b 位收拢到第 k 位
}
```

`expand` 是反过来：第 k 位散开到第 b 位。`reverse` 用交换相邻位、相邻 2 位、相邻 4 位……的分步法或简单循环；`bswap` 用移位和掩码。`CTZ` / `CLZ` 直接 `std::countr_zero` / `std::countl_zero`，对 0 返回 32。

**面试官在探什么**

1. **`m &= m - 1` 为什么对**。`m - 1` 把最低位的 1 变成 0、其下的 0 全变成 1，与 `m` 相与恰好清掉最低位的 1。循环次数等于掩码里 1 的个数，不用扫 32 位。
2. **compress 和 expand 的关系**。`expand(compress(x, m), m) == x & m`；这是最好的随机测试。x86 的 BMI2 上它们对应 `PEXT` / `PDEP` 一条指令。
3. **对 0 的约定**。`std::countr_zero(0u)` 是 32；`__builtin_ctz(0)` 是 UB。
4. **手算例**：`0x12345678` 先 `BSWAP` 得 `0x78563412`，`CTZ` 是 1（最低字节 `0x12` 的二进制末尾有 1 个 0）；`COMPRESS 0x0F0F0F0F` 取每字节的低半字节 2、4、6、8，得 `0x8642`；`REVERSE` 得 `0x42610000`，`CLZ` 是 1。
5. **大小端对 `BSWAP` 有没有关系**。语义是固定的（翻转字节顺序），和机器无关；有关系的是把寄存器写进字节缓冲区，要用 `memcpy` 加 `std::endian` 判断，或者统一用移位拆字节。

**该说出口的话**：「标准库没有 compress，我循环处理掩码里的每一位，用 `m &= m - 1` 每次清一个；对 0 的 ctz / clz 用 `<bit>`，它们有定义。」

## Part 4 · 解码一次，热循环不分配

**写法**：`compile` 把每条指令变成 (操作码, 操作数)：`NOT` 折叠成 `XOR 0xFFFFFFFF`，`SET b` 折叠成 `OR (1<<b)`，`CLEAR b` 折叠成 `AND ~(1<<b)`，`TOGGLE b` 折叠成 `XOR (1<<b)`；移位位数夹到 [0, 32]，旋转位数 `& 31`。`execute` 一个循环加一个 `switch`：

```cpp
case OP_SHL: reg = static_cast<Reg>(static_cast<std::uint64_t>(reg) << a); break;   // a <= 32：64 位移位有定义
case OP_SHR: reg = static_cast<Reg>(static_cast<std::uint64_t>(reg) >> a); break;
default: throw std::logic_error("bad opcode");                                       // 不能乱跳
```

**面试官在探什么**

1. **为什么这样更快**。类型分发、对象读取、折叠掉的几种指令都挪出了热循环；连续的 `uint32_t` 对预取友好，每条指令占 8 字节，`variant` 版占 16 字节。
2. **移位为什么没有分支也没有 UB**。位数已夹到 ≤ 32，64 位移位对 ≤ 32 有定义；左移 32 把原来的 32 位全推到高半部分，截断后全是 0；右移 32 同理。
3. **哪里还会慢**。`switch` 本身是一次间接跳转，操作码序列随机时分支预测器会猜错，这才是主要开销。「无分支」指的是指令语义内部，不是指分发。
4. **再往下怎么优化**。把相邻的纯位运算融合成 `r = (r & a) ^ x` 一条；threaded code（computed goto）；对热点程序直接生成机器码。要如实说，不要夸大数组版的收益。
5. **结果必须和 `run` 完全一样**：用同一批随机程序对拍，包括位数 `INT_MAX` 这类极端值。
6. **损坏的操作码**：`default` 抛异常，不要让 `switch` 落空后继续用旧值。

**该说出口的话**：「解码一次，热循环里只有数组读取和一个 switch；移位在 64 位里做，位数已经夹到 32，所以没有分支也没有 UB；剩下的瓶颈是分支预测。」

## stdin → stdout 形式

`cpp/main.cpp` 只做一件事：读入 stdin 的所有行，调用 `solve`，每个结果一行写到 stdout。要点：

1. **空 stdin** 也要输出 `Malformed Input`，不能因为没有第一行而崩溃。
2. **最后一行没有换行**、CRLF 行尾都要正常处理；`getline` 不会保留 `\n`，但会保留 `\r`。
3. 输出行以 `\n` 结尾，对拍是逐字节比较。
4. 用 `python3 tools/cpptest.py main <题目目录> --impl work < cases/xxx.in` 跑，和对应的 `.out` 比较。

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 寄存器类型 | `int`（有符号，按无符号解释） | `std::uint32_t`（真无符号） |
| 逻辑右移 | `>>>` | `>>`（无符号类型） |
| 移位位数 ≥ 32 | 位数取低 5 位，`x << 32 == x` | UB，必须显式处理 |
| 无符号打印 | `Integer.toUnsignedString` | `std::to_string(uint32_t)` |
| 旋转 | `Integer.rotateLeft` | `std::rotl`（`<bit>`） |
| 计数 | `bitCount` / `numberOfTrailingZeros` | `std::popcount` / `countr_zero`；`__builtin_ctz(0)` 是 UB |
| compress / expand / reverse / bswap | `Integer.compress` 等现成 | 标准库没有（`std::byteswap` 是 C++23），自己写 |
| 数字解析 | `Long.parseLong` + 范围检查 | `std::from_chars` + 检查结束指针；不认 `+` |
| 指令层次 | `sealed interface` + `record` | `std::variant` + 小结构体 |
| 穷尽匹配 | 模式匹配 `switch` | `std::visit(overloaded{...})`，漏一个类型编译失败 |
| 字符分类 | `Character.digit` | 自己写 ASCII 版；`std::isspace(char)` 传负数是 UB |
