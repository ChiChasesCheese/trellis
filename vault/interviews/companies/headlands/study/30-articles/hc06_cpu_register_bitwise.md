# hc06 · CPU 寄存器位运算 —— 讲义

> 题面：`loop/rounds/01_video/hc06_cpu_register_bitwise/problem.md` · 速查：同目录 `REPORT.md` · 代码：同目录 `reference/RegisterSim.java`
> 写法说明见 `study/TEXTBOOK.md`。读者设定：会写基本 Java，不懂二进制也没关系——第 2 节从“什么是 bit”讲起。
> 证据说明：公开信息只有题目名「CPU Register Bitwise Operations」和一句“模拟一个无符号 32 位寄存器，给定初值”；
> 指令集、输入输出格式、扩展指令、性能版本都是 **(reconstructed)**。

---

## 1. 这道题在问什么

CPU 里有叫**寄存器**（register）的小存储单元，一个 32 位寄存器就是 **32 个开关**，每个开关要么开（1）要么关（0）。
题目给你寄存器的初值和一串指令（“把某几个开关关掉”“整体往左挪 4 格”“数一数有几个开关是开的”……），让你依次执行，最后输出结果。

### 手算一遍

初值 `0xF0`（十六进制，等于十进制 240）。程序：

```
AND 0x3C
SHL 4
OR 0x0F
POPCOUNT      → 输出 1 的个数
NOT
SHR 28
POPCOUNT
```

把它写成二进制（只写低 12 位，高位全是 0）：

```
初值        0xF0        0000 1111 0000
AND 0x3C    0x3C        0000 0011 1100      逐位“都是 1 才是 1”
            结果 0x30   0000 0011 0000
SHL 4       整体左移 4  0011 0000 0000      = 0x300
OR 0x0F     0x0F        0000 0000 1111      逐位“有一个 1 就是 1”
            结果 0x30F  0011 0000 1111
POPCOUNT    数 1 的个数：2 + 4 = 6          → 输出 6
NOT         每位取反    32 位：1111 1111 1111 1111 1111 1100 1111 0000 = 0xFFFFFCF0
SHR 28      右移 28 位，只剩最高的 4 位 1111 = 0xF
POPCOUNT    4 个 1                          → 输出 4
终值 0xF = 十进制 15
```

输出：`6`、`4`，最后一行 `0x0000000F 15 00000000000000000000000000001111`（十六进制、十进制、32 位二进制）。

这道题难在哪？**每一步都有一个 Java 特有的坑**：`NOT` 之后的数在 Java 的 `int` 里是**负数**；`SHR` 如果写成 `>>` 会把高位补成 1；`SHL 32` 在 Java 里不是 0……后面逐个讲。

---

## 2. 前置知识

### 2.1 二进制、bit、字节、十六进制

**是什么**：bit（位）是只能取 0 或 1 的最小单位。n 个 bit 排成一排可以表示 2ⁿ 个不同的值。8 个 bit 叫一个**字节**（byte）。
我们像十进制一样用“位权”读它：从右往左，第 0 位权重 1，第 1 位权重 2，第 2 位权重 4……第 k 位权重 2ᵏ。

```
位号:     7    6    5    4    3    2    1    0
位权:   128   64   32   16    8    4    2    1
        0    0    1    0    1    1    0    1       = 32 + 8 + 4 + 1 = 45
```

**为什么需要十六进制**：32 位二进制太长（32 个字符），人读不过来。十六进制每位对应**恰好 4 个 bit**，所以 32 位正好 8 个十六进制字符，而且能一位一位直接换算：

```
二进制  0000 0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111
十六进制  0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F

0xDEADBEEF = 1101 1110 1010 1101 1011 1110 1110 1111
              D    E    A    D    B    E    E    F
```

**Java 里怎么写**：

```java
int a = 0xFF;          // 十六进制字面量，255
int b = 0b1010;        // 二进制字面量，10
int c = 0xFFFFFFFF;    // 注意：这是个 int 字面量，值是 -1（见 2.2）
```

### 2.2 补码、有符号与无符号：同样的 32 个 bit，两种读法

**是什么**：Java 的 `int` 有 32 个 bit，但要同时表示正数和负数。规则（**补码**，two's complement）：最高位（第 31 位）的权重是**负的** −2³¹，其余位权重照旧。
用 8 位演示更好看：

```
位号:         7     6    5    4    3    2    1    0
位权(有符号): −128   64   32   16    8    4    2    1
位权(无符号):  128   64   32   16    8    4    2    1

位模式  1111 1111
  当有符号数读：−128 + 64+32+16+8+4+2+1 = −1
  当无符号数读： 128 + 64+32+16+8+4+2+1 = 255

位模式  1000 0000
  有符号：−128          无符号：128
位模式  0111 1111
  有符号：127           无符号：127            ← 最高位是 0 时两种读法相同
```

32 位同理：`0xFFFFFFFF`——有符号读是 **−1**，无符号读是 **4 294 967 295**；`0x80000000`——有符号 −2 147 483 648，无符号 2 147 483 648。

**为什么这对本题至关重要**：题目说寄存器是**无符号 32 位**，值域 0..4 294 967 295。Java **没有无符号 int**。
但没关系：32 个 bit 是一样的，只是“怎么解释”不同。所以我们用 `int` 存位模式，约定：

1. 做位运算（`& | ^ ~ <<`）时，有符号还是无符号没区别——它们只看 bit。
2. **右移**（`>>` 与 `>>>`）、**比较大小**、**转十进制字符串 / 转 `long`** 这三类操作，有符号还是无符号**结果不同**，必须显式选无符号版本。

**Java 里怎么写**：

```java
int reg = 0xFFFFFFFF;                        // 位模式全 1，值是 -1
long u = Integer.toUnsignedLong(reg);        // 4294967295L：先零扩展到 64 位
String s = Integer.toUnsignedString(reg);    // "4294967295"
Integer.compareUnsigned(0x80000000, 1) > 0;  // true：按无符号 2147483648 > 1
```

注意：`(long) reg` 是**错的**——它会做符号扩展，得到 `-1L`。

### 2.3 位运算：AND、OR、XOR、NOT

**是什么**：对两个数的**每一位独立**做布尔运算：

```
  a   b | a&b  a|b  a^b          ~a
  0   0 |  0    0    0           1
  0   1 |  0    1    1           0
  1   0 |  0    1    1
  1   1 |  1    1    0
  &：都是 1 才是 1      |：有一个 1 就是 1      ^（异或）：不同才是 1      ~：取反
```

```
  1100        1100        1100
& 1010      | 1010      ^ 1010      ~ 1100 (4 位) = 0011
------      ------      ------
  1000        1110        0110
```

**为什么需要它们**：它们是“操作一堆开关”的原语：`&` 用来**关掉**不想要的开关、`|` 用来**打开**开关、`^` 用来**翻转**开关。

**Java 里怎么写**：`reg & mask`、`reg | mask`、`reg ^ mask`、`~reg`。`~reg` 对 32 位 int 翻转全部 32 位（`~0 == 0xFFFFFFFF == -1`）。

### 2.4 掩码（mask）与单个 bit 的操作

**是什么**：掩码是一个“选哪几位”的模板。要操作第 b 位，造一个只有第 b 位是 1 的掩码：`1 << b`。

| 操作 | 公式 | 为什么 |
|---|---|---|
| 置 1（SET） | `reg \| (1 << b)` | OR 1 → 一定是 1，其他位 OR 0 → 不变 |
| 清 0（CLEAR） | `reg & ~(1 << b)` | `~(1<<b)` 是“只有第 b 位是 0”的掩码，AND 它只清第 b 位 |
| 翻转（TOGGLE） | `reg ^ (1 << b)` | XOR 1 → 翻转，XOR 0 → 不变 |
| 测试 | `(reg >>> b) & 1` | 把第 b 位挪到最低位再 AND 1 |

```
reg = 1011 0110 (8 位演示)，b = 3，1<<3 = 0000 1000
SET    reg | 0000 1000 = 1011 1110
CLEAR  reg & 1111 0111 = 1011 0110   （第 3 位本来就是 0，没变）
TOGGLE reg ^ 0000 1000 = 1011 1110
```

**坑**：`1 << 31` 是 `0x80000000`，在 `int` 里是**负数** `−2147483648`，但位模式正是“只有最高位”，作为掩码完全正确。位号必须在 0..31：`1 << 32` 在 Java 里等于 `1 << 0 == 1`（见 2.5），位号 32 要在入口就拒绝。

### 2.5 移位：`<<`、`>>`、`>>>`

**是什么**：把所有 bit 整体向左或向右挪 n 格。挪出去的丢掉；空出来的格子补什么，分三种：

```
8 位演示，x = 1011 0110 (0xB6)

x << 2   左移：低位补 0，高位挪出的丢掉         = 1101 1000   （最高 2 位 "10" 丢了）
x >>> 2  逻辑右移：高位补 0                     = 0010 1101
x >> 2   算术右移：高位补“原来的最高位”（符号位）= 1110 1101   （x 最高位是 1，补 1）
```

* `>>>`（逻辑右移 logical）：永远补 0。把 bit 当“一排开关”时用它——**寄存器就该用这个**。
* `>>`（算术右移 arithmetic）：补符号位。作用：对有符号数做“除以 2ⁿ（向下取整）”时保持符号。对负数补 1。
  `0xF0000000 >> 4 = 0xFF000000`，**不是**我们要的 `0x0F000000`。

**为什么需要关心**：寄存器最高位是 1 时（如 `NOT` 之后），用 `>>` 会把垃圾位 1 带进来，结果错误。

**Java 的特殊规则（重要！）**：对 `int`，移位的位数**只取低 5 位**，即 `n & 31`。所以：

```java
int x = 0xFFFFFFFF;
x << 32    // == x << 0 == 0xFFFFFFFF，不是 0！
x << 33    // == x << 1
x >>> 32   // == x
```

C/C++ 里，位数 ≥ 位宽是**未定义行为**。而题目（真实的硬件语义）要的是：移 32 位或更多，32 个 bit 全部被挤出去，结果 0。所以要自己判断（`n >= 32 ? 0 : x << n`），或者用 `long` 做（见第 4 节步骤 7）。

### 2.6 旋转（rotate）

**是什么**：像移位，但挪出去的 bit 从另一头**绕回来**，一个 bit 都不丢。

```
x = 0x12345678 = 0001 0010 0011 0100 0101 0110 0111 1000
ROL 4（循环左移 4 位）：最高的 4 位 0001 绕到最低位
  = 0010 0011 0100 0101 0110 0111 1000 0001 = 0x23456781
ROR 4：最低的 4 位 1000 绕到最高位
  = 1000 0001 0010 0011 0100 0101 0110 0111 = 0x81234567
```

位数对 32 取模：`ROL 32` 转了一整圈 = 不变；`ROL 36 == ROL 4`。

**Java 里怎么写**：`Integer.rotateLeft(x, n)`、`Integer.rotateRight(x, n)`——已经按 `n mod 32` 处理，而且是 JIT intrinsic，在 x86 / ARM 上编译成一条旋转指令。
自己手写成 `(x << n) | (x >>> (32 - n))` 也可以，但 `n == 0` 时 `x >>> 32 == x`（Java 的 mod 32 规则），结果是 `x | x == x`，碰巧正确；换成 `>>` 就会出错。

### 2.7 计数与重排：popcount、ctz、clz、reverse、bswap、compress、expand

* **popcount**（population count）：数有几个 1。`Integer.bitCount(x)`。CPU 有专门的 `POPCNT` 指令，JIT 会用它。
  `bitCount(0) == 0`，`bitCount(-1) == 32`。
* **ctz**（count trailing zeros，末尾 0 的个数）：`Integer.numberOfTrailingZeros(x)`。等价于“最低的 1 在第几位”。`x == 0` 时返回 **32**。
* **clz**（count leading zeros，前导 0 的个数）：`Integer.numberOfLeadingZeros(x)`。`x == 0` 时 32；`x < 0`（最高位是 1）时 0。
* **reverse**：32 个 bit 整体倒过来，第 0 位和第 31 位交换……`Integer.reverse(x)`。`reverse(1) == 0x80000000`。
* **bswap**（byte swap，字节序翻转）：4 个字节顺序倒过来，字节内部不变。`Integer.reverseBytes(x)`：`0x12345678 → 0x78563412`。网络协议常用（大端 / 小端互转）。
* **compress / expand**（Java 19 起）：这两个是“按掩码收拢 / 散开”。
  `compress(x, mask)`：取出 x 中 mask 为 1 的那些位，**按顺序**挤到结果的低位。

  ```
  x    = 1011 0110 (0xB6)
  mask = 1111 0000 (0xF0)         mask 为 1 的位置：7 6 5 4
  取出 x 的这些位：1 0 1 1        → 结果 0000 1011 = 0xB

  散开的掩码：
  x    = 1101 0110 (0xD6)
  mask = 1010 1010 (0xAA)         mask 为 1 的位置：7 5 3 1（从高到低）
  x 在这些位置的值：pos1=1, pos3=0, pos5=0, pos7=1
  按位置从低到高排进结果的第 0,1,2,3 位：1 0 0 1 → 0b1001 = 9
  ```

  `expand(v, mask)` 反过来：把 v 的低位依次放进 mask 为 1 的位置，其余位置补 0。性质：`expand(compress(x, m), m) == x & m`。
  x86 的 BMI2 指令集有 `PEXT/PDEP` 一条指令完成它；其他平台走软件实现。

### 2.8 字符串里的数怎么读：进制、范围、为什么用 long

**是什么**：输入里的数可能是 `255`、`0xFF`、`0b11111111`。解析它们要：识别前缀决定进制、检查每个字符合法、检查范围。

**为什么不用 `Integer.parseInt`**：它的结果是有符号 `int`，范围 −2³¹..2³¹−1。`Integer.parseInt("4294967295")` 和 `Integer.parseInt("FFFFFFFF", 16)` 都会抛 `NumberFormatException`——但这两个都是 32 位寄存器的合法值。
所以：用 `Long.parseLong(digits, radix)` 读成 `long`（64 位，装得下 0..4294967295），检查 `0 ≤ v ≤ 0xFFFFFFFFL`，最后 `(int) v` 强转——强转只保留低 32 位，位模式原样保留。

**也不用 `Long.decode`**：它把前导 0 当八进制（`"010"` 是 8），还接受 `-` 和 `#`；我们要严格的小语言。
**还要**：逐字符检查是否合法数字（`Character.digit(c, radix)`），因为 `Long.parseLong` 接受 `+1`。

### 2.9 CPU 的分支预测与缓存（只为第 4 部分，概览）

**流水线**：CPU 不是做完一条指令再做下一条，而是像流水线一样同时处理十几条指令的不同阶段。遇到**分支**（`if`、`switch` 的跳转）时，CPU 还不知道接下来走哪条路，就**猜**一个，继续往下流水。
**分支预测**：猜对了，白赚；猜错了，已经在流水线里做了一半的指令全部作废重来，代价约十几个时钟周期。预测器靠历史规律猜：规律的序列（每次都走同一边，或周期性）猜得准；随机序列几乎只能蒙。

**缓存**：CPU 读内存很慢，所以读一个字节时会顺便把它附近的一整行（通常 64 字节）拉进缓存。连续存放的 `int[]`：读完第 k 个，第 k+1..k+15 个都已经在缓存里了。
对象数组 `Object[]`：数组里存的是引用（指针），每个对象在堆上不同位置，读每个都可能要再去一次内存，还要读对象头判断类型。

### 2.10 本题用到的 Java 语法速览

`record`、`sealed interface … permits`、`switch` 对 sealed 类型的模式匹配（`case And(var m) -> …`，无需 `default`）、`switch` 表达式、文本块、`HexFormat`。
细节见第 6 节与 `study/10-java21/` 中对应的 J01–J05、J07、J15 篇。

---

## 3. 从最笨的解法开始

大多数人第一反应：用字符串比较指令名，用 `int` 存寄存器，用 `Integer.parseInt` 读数，用 `println` 输出。

```java
int reg = Integer.parseInt(lines.get(0));
for (String line : lines.subList(1, lines.size())) {
    String[] p = line.split(" ");
    if (p[0].equals("AND"))      reg = reg & Integer.parseInt(p[1]);
    else if (p[0].equals("OR"))  reg = reg | Integer.parseInt(p[1]);
    else if (p[0].equals("XOR")) reg = reg ^ Integer.parseInt(p[1]);
    else if (p[0].equals("NOT")) reg = ~reg;
    else if (p[0].equals("SHL")) reg = reg << Integer.parseInt(p[1]);
    else if (p[0].equals("SHR")) reg = reg >> Integer.parseInt(p[1]);
    else if (p[0].equals("POPCOUNT")) System.out.println(Integer.bitCount(reg));
}
System.out.println(reg);
```

* **复杂度**：解析 + 执行 O(m)（m = 指令数），每条指令 O(1)；空间 O(1)。时间上没问题。
* **它在这些输入上是错的**：

| 输入 | 期望 | 这份代码 | 原因 |
|---|---|---|---|
| 初值 `4294967295` | 合法 | 抛 `NumberFormatException` | `parseInt` 范围是有符号 int（2.8） |
| `AND 0xFFFFFFFF` | 合法 | 抛异常，且 `parseInt` 不认 `0x` 前缀 | 同上 |
| 初值 `0x80000000`，`SHR 31` | 1 | `-1` | `>>` 补符号位（2.5） |
| 初值 `1`，`SHL 32` | 0 | 1 | Java 移位位数只取低 5 位（2.5） |
| 终值 `0xFFFFFFFF` | `4294967295` | `-1` | 没有用无符号输出（2.2） |
| `SET 32` | `Malformed Input` | （没有这条指令；加上后 `1 << 32 == 1` 悄悄置了第 0 位） | 位号越界没检查 |
| 指令 `FOO` | `Malformed Input` | 默默忽略 | 没有 `else` |
| `ROL 36` | 同 `ROL 4` | 没实现 | |

结论：位运算本身是一行代码，**全部的难度在边界**。

---

## 4. 一步一步改进

### 步骤 1：数字解析——用 `long`，严格校验

* **发现问题**：`Integer.parseInt` 读不了 32 位无符号数，也不认 `0x`、`0b` 前缀。
* **想法**：自己写 `parseValue`：识别前缀 → 逐字符检查 → `Long.parseLong` → 范围 `0..0xFFFFFFFFL` → 返回 `long`。
* **为什么能解决**：`long` 有 64 位，装得下任何 32 位无符号数；强转 `(int)` 时位模式原样保留。
* **边界**：`"010"` 是十进制 10；`"0x"` 单独出现非法；`"-1"`、`"+1"` 非法；`"4294967296"` 非法。

### 步骤 2：把指令从“字符串”变成“类型”

* **发现问题**：字符串比较散落各处；每执行一条指令都要重新比较；拼写错误（`"ShR"`）编译器发现不了；非法指令（`SET 32`）要到执行时才发现。
* **想法**：每种指令一个 `record`，全部实现 sealed 接口 `Instr`。非法值在**构造时**由记录的紧凑构造器拒绝：

  ```java
  public record SetBit(int bit) implements Update {
      public SetBit { if (bit < 0 || bit > 31) throw new IllegalArgumentException("bit out of 0..31: " + bit); }
  }
  ```

* **执行**：对 sealed 接口写 `switch`，编译器检查每种指令都有分支：

  ```java
  case And(var m) -> reg & m;
  case Shl(var n) -> n >= 32 ? 0 : reg << n;
  ```

* **再拆一层**：指令分两类——会改寄存器的 `Update`，只读并输出一个数的 `Query`（`POPCOUNT` 等）。`apply(int reg, Update u)` 返回新的寄存器值；`query(int reg, Query q)` 返回要输出的数。类型就说明了“这条指令会不会改寄存器”。
* **新复杂度**：不变，O(m)。解析一次、执行一次。

### 步骤 3：无符号语义

* **`SHR`**：用 `reg >>> n`（2.5），不用 `>>`。
* **输出**：十进制用 `Integer.toUnsignedString(reg)`；转 `long` 用 `Integer.toUnsignedLong(reg)`。
* **十六进制**：`HexFormat.of().withUpperCase().toHexDigits(reg)`——对 `int` 固定输出 8 个字符，自动补零，且把 int 当位模式（不带负号）。加上前缀 `"0x"`。
* **二进制**：`Integer.toBinaryString(reg)` 不补前导零（5 → `"101"`），要手动补到 32 位。用 `StringBuilder.repeat('0', 32 - raw.length())`。

### 步骤 4：移位位数 ≥ 32

* **发现问题**：Java 里 `reg << 32 == reg`。
* **想法 A（简单）**：`n >= 32 ? 0 : reg << n`。分支，但清楚。
* 想法 B 留到步骤 8（性能版本）：用 `long` 做移位，免分支。

### 步骤 5：旋转

* `Integer.rotateLeft(reg, n)` / `rotateRight`——它们本来就取 `n mod 32`，`ROL 36 == ROL 4`；这也是 JIT intrinsic。
* 手写 `(reg << n) | (reg >>> (32 - n))` 也行，但要处理 `n % 32 == 0`（`>>> 32` 是 `>>> 0`，碰巧对，但要有意识）。

### 步骤 6：整合输出与错误处理

* `solve(lines)`：第一个有效行是初值，其余是程序。每个 Query 的输出一行十进制，最后一行 `describe(终值)`（`hex dec bin`）。
* 任何 `MalformedProgramException` → 只输出 `Malformed Input`。解析阶段捕获记录构造器抛的 `IllegalArgumentException`，转成 `MalformedProgramException`。

### 步骤 7：扩展指令，别手写

* `COMPRESS / EXPAND / REVERSE / BSWAP / CTZ / CLZ` 直接用 `Integer.compress/expand/reverse/reverseBytes/numberOfTrailingZeros/numberOfLeadingZeros`（2.7）。
* 因为 `Instr` 是 sealed，新增这 6 个 record 后，`apply` 和 `query` 的 `switch` **立刻编译报错**，逼你把分支补全——这正是 sealed 的价值。
* 面试官看的是：你知道标准库里已经有，不会去写一个 20 行的循环。

### 步骤 8：性能——解码一次，`int[]`，无分支

* **发现问题**：假设程序有 1000 万条指令，或同一个程序要对大量初值各跑一遍。`run()` 的每一步：从 `List<Instr>` 取一个对象（指针追逐）、`switch` 做类型分派、record 解构。能不能把这些挪出热循环？
* **想法**：**编译**一次，把程序变成两个 `int[]`：`ops[]`（操作码 0..13）和 `args[]`（操作数）。热循环里只有数组读写和一个 `switch (ops[pc])`，不创建对象。
* **解码时就能做的化简**：
  * `NOT` = `XOR 0xFFFFFFFF`；`SET b` = `OR (1<<b)`；`CLEAR b` = `AND ~(1<<b)`；`TOGGLE b` = `XOR (1<<b)`。操作码从 18 种降到 14 个。
  * 移位位数 `Math.clamp(c, 0, 32)`；旋转位数 `c & 31`。
* **移位免分支**：

  ```java
  case SHL -> reg = (int) (Integer.toUnsignedLong(reg) << a);   // a ∈ [0, 32]
  case SHR -> reg = (int) (Integer.toUnsignedLong(reg) >>> a);
  ```

  `Integer.toUnsignedLong(reg)` 把 32 位零扩展到 64 位；`long` 的移位位数最多 63，所以 `<< 32` 真的移 32 位：原来的 32 个 bit 全推到高半部分，`(int)` 强转只留低 32 位，结果 0。右移 32 同理。不需要 `if (n >= 32)`。
* **实测**（本机，200 万条指令，预热后）：

  | 程序形态 | `run`（对象 + 模式匹配） | `execute`（`int[]`） |
  |---|---|---|
  | 随机 18 种指令 | 21 ms | 14 ms |
  | 随机，只含 14 种更新型指令 | 17 ms | 11 ms |
  | 固定循环的 14 条指令（周期序列） | 9 ms | **1 ms** |

* **解读**：规律序列上快了 9 倍；随机序列只快 1.5 倍。因为 `switch` 本身编译成一条**间接跳转**：操作码序列随机时，CPU 的分支预测器大量猜错（2.9），每次错误损失十几个周期，把 `int[]` 省下的时间吃掉一大半。
  所以“无分支”指的是**指令语义内部**（移位、位号）无分支，不是指分发。
* **还能更快吗**：把相邻的 `AND/OR/XOR/NOT/SET/CLEAR/TOGGLE` 融合成一条 `r = (r & a) ^ x`（这几种操作的任意复合仍是这个形式）；常量折叠；把整个程序编译成字节码，让 JIT 去掉分发。这些是面试时可以口头提的方向，本题不要求实现。

---

## 5. 逐段讲参考解

### 5.1 指令层次

```java
public sealed interface Instr permits Update, Query {}
public sealed interface Update extends Instr
        permits And, Or, Xor, Not, Shl, Shr, Rol, Ror, SetBit, ClearBit, ToggleBit, Compress, Expand, Reverse, ByteSwap {}
public sealed interface Query extends Instr permits Popcount, TrailingZeros, LeadingZeros {}

public record And(int mask) implements Update {}
public record Not() implements Update {}
public record SetBit(int bit) implements Update {
    public SetBit { checkBit(bit); }       // 紧凑构造器：校验位号
}
```

* 两层 sealed：`Instr` 只能是 `Update` 或 `Query`；`Update` 只能是 15 个 record 之一。编译器在 `switch` 里能逐层检查是否穷尽。
* `record Not()` 没有字段：只表示“这是 NOT 指令”。
* `public SetBit { … }` 是紧凑构造器：在字段赋值**之前**运行校验；非法的 `SetBit(32)` 根本构造不出来。
* 为什么分 `Update`/`Query`：它们的“返回值含义”不同——一个是新寄存器值，一个是要输出的数。分开后 `apply` 和 `query` 各自的返回类型明确。

### 5.2 `parseValue` 与 `parseLine`

```java
if (t.length() > 2 && t.charAt(0) == '0') {
    switch (t.charAt(1)) {
        case 'x', 'X' -> { radix = 16; digits = t.substring(2); }
        case 'b', 'B' -> { radix = 2;  digits = t.substring(2); }
        default -> { }
    }
}
for (int i = 0; i < digits.length(); i++)
    if (Character.digit(digits.charAt(i), radix) < 0) throw new MalformedProgramException(...);
long v = Long.parseLong(digits, radix);
if (v > 0xFFFF_FFFFL) throw new MalformedProgramException(...);
```

* `t.length() > 2`：让 `"0x"` 单独出现时不进入前缀分支，之后按十进制解析，`'x'` 不是数字，被拒。
* 逐字符检查是为了拒绝 `+1`、`-1`、`1_0` 这类不属于小语言的写法（`Long.parseLong` 本身接受 `+` 和 `-`）。
* 数字太长（超过 `long`）时 `parseLong` 抛 `NumberFormatException`，被转成 `MalformedProgramException`。

```java
return switch (p[0].toUpperCase(Locale.ROOT)) {
    case "AND" -> new And(mask(p));
    case "NOT" -> bare(p, new Not());
    case "SHL" -> new Shl(small(p));
    ...
    default -> throw new MalformedProgramException("unknown instruction: " + p[0]);
};
```

* `Locale.ROOT`：避免土耳其语等语言环境下 `"i".toUpperCase()` 变成带点的 `İ`。
* `mask(p)` 读 `parseValue`，然后 `(int)` 强转——`0xFFFFFFFF` 变成 `And(-1)`，位模式全 1，正是想要的掩码。
* `small(p)` 读位数 / 位号：纯十进制数字，且必须装进 `int`。

### 5.3 `apply`

```java
public static int apply(int reg, Update u) {
    return switch (u) {
        case And(var m)    -> reg & m;
        case Not _         -> ~reg;
        case Shl(var n)    -> n >= 32 ? 0 : reg << n;
        case Shr(var n)    -> n >= 32 ? 0 : reg >>> n;
        case Rol(var n)    -> Integer.rotateLeft(reg, n);
        case SetBit(var b) -> reg | (1 << b);
        case ClearBit(var b)  -> reg & ~(1 << b);
        case ToggleBit(var b) -> reg ^ (1 << b);
        case Compress(var m)  -> Integer.compress(reg, m);
        ...
    };
}
```

* 没有 `default`：`Update` 是 sealed，编译器保证 15 种都覆盖了。
* `case Not _`：`_` 表示“我不关心 `Not` 里的字段（它本来也没有）”，是 Java 21 预览特性。
* `n >= 32 ? 0 : …`：在语义层面明确“≥ 32 得 0”。
* `Integer.rotateLeft` 对任意 `int` 位数都按 mod 32 处理，所以 `Rol(Integer.MAX_VALUE)` 也安全。

### 5.4 `run`

```java
int reg = checkedInitial(initial);
var out = new ArrayList<Integer>();
for (Instr i : program) {
    switch (i) {
        case Update u -> reg = apply(reg, u);
        case Query q  -> out.add(query(reg, q));
    }
}
return new Run(reg, List.copyOf(out));
```

* `checkedInitial` 检查 `0 ≤ initial ≤ 0xFFFFFFFFL`，再 `(int)` 强转保位模式。初值用 `long` 传进来的原因：4294967295 放不进非负 `int`。
* 外层 `switch` 只有两个分支（`Update`、`Query`），因为 `Instr` 只 `permits` 这两个子接口。
* `List.copyOf` 给调用方一个不可变列表。

### 5.5 格式化

```java
public static String hex(int reg) { return "0x" + HexFormat.of().withUpperCase().toHexDigits(reg); }
public static String bin(int reg) {
    String raw = Integer.toBinaryString(reg);
    return new StringBuilder(32).repeat('0', 32 - raw.length()).append(raw).toString();
}
public static String dec(int reg) { return Integer.toUnsignedString(reg); }
```

* `HexFormat.toHexDigits(int)`：固定 8 位、补零、按位模式输出（`-1 → "FFFFFFFF"`）。
* `StringBuilder.repeat(char, int)`（Java 21）：旧写法 `"0".repeat(n)` 要多创建一个字符串。
* `Integer.toBinaryString(-1)` 本来就是 32 个 `1`（把 int 当位模式，不带负号），`raw.length()` 是 32，补 0 个 `0`。

### 5.6 `compile` / `execute`

```java
public record Compiled(int[] ops, int[] args, int queryCount) {}

case Not _          -> { ops[k] = XOR; args[k] = -1; }
case SetBit(var b)  -> { ops[k] = OR;  args[k] = 1 << b; }
case Shl(var c)     -> { ops[k] = SHL; args[k] = Math.clamp(c, 0, 32); }
case Rol(var c)     -> { ops[k] = ROL; args[k] = c & 31; }
```

* 两个平行数组：第 k 条指令的操作码 `ops[k]`、操作数 `args[k]`，在内存里都是连续的 `int`（缓存友好，2.9）。
* `Math.clamp(c, 0, 32)`（Java 21）：把位数夹到 `[0, 32]`。旧写法 `Math.min(Math.max(c, 0), 32)`。
* `queryCount` 预先数好，执行时一次性分配好输出数组 `new int[c.queryCount()]`，热循环里不扩容。

```java
for (int pc = 0; pc < ops.length; pc++) {
    int a = args[pc];
    switch (ops[pc]) {
        case AND -> reg &= a;
        case SHL -> reg = (int) (Integer.toUnsignedLong(reg) << a);
        case POPCOUNT -> out[q++] = Integer.bitCount(reg);
        ...
    }
}
```

* `switch` 对 `int` 常量：编译成 `tableswitch`（跳转表）。
* 热循环里没有 `new`（`Run` 在循环外创建），也没有类型检查。
* 返回时 `Arrays.stream(out).boxed().toList()` 把 `int[]` 装箱成 `List<Integer>`，只做一次，在循环外。

---

## 6. Java 21 特性小课

### J01 record + 紧凑构造器

旧写法：为每条指令写一个带 `equals/hashCode/toString` 的 final 类，字段校验写在构造器里。新写法：`record SetBit(int bit) { SetBit { checkBit(bit); } }`。
测试里 `assertEquals(new And(0xFF), RegisterSim.parseLine("AND 0xFF"))` 直接比较，靠的是 record 自动生成的 `equals`。
**不该用**：要继承其他类、需要可变字段时。

### J02 sealed

旧写法：`enum Op { AND, OR, … }` 加一堆可空字段（`Integer mask; Integer count;`），或 `interface Instr` 配 `instanceof` 链加最后一个 `else throw`。
新写法：`sealed interface … permits …`。编译器知道所有实现；写 `switch` 时漏一种就编译失败。

### J03 + J04 switch 模式匹配 + record 解构

`case And(var m) -> reg & m;`：一次完成“是不是 And”“取出 mask”。无需强转，无需 `default`。
**不该用**：`default` 兜底（会让编译器不再提醒你漏了新指令）。

### J05 switch 表达式

`return switch (u) { case … -> …; };` 每个分支是值，没有 `break`，不会 fallthrough。旧写法每个 `case` 要 `break`，忘一个就串到下一个。

### J13 未命名模式 `_`（预览）

`case Not _ ->`、`case Popcount _ ->`：这些 record 没有需要的字段，用 `_` 说明“不绑定”。需要 `--enable-preview`（`jtest.py` 已加）。

### J15 位运算与数学小工具

`Integer.compress/expand`（Java 19）、`rotateLeft`、`reverse`、`reverseBytes`、`bitCount`、`HexFormat`（Java 17）、`Integer.toUnsignedString`、`Math.clamp(long,int,int)`（Java 21）、`StringBuilder.repeat`（Java 21）。
旧写法都要手写循环或位技巧，容易出错且无法用到 CPU 的专用指令。

### J14 Stream / J07 文本块 / J09 Sequenced Collections

`Arrays.stream(out).boxed().toList()`；测试里用文本块写多行程序；`solve` 里用 `body.getFirst()` 代替 `body.get(0)`。

---

## 7. 追问预演

**Q1：Java 没有 unsigned int，你怎么处理？**

* 思考过程：先想“什么是真正需要无符号的操作”——只有右移、比较、转十进制 / long。位运算本身不区分。
* 答案要点：用 `int` 存位模式；右移用 `>>>`；转 `long` 用 `Integer.toUnsignedLong`；打印用 `Integer.toUnsignedString`；比较用 `Integer.compareUnsigned`；64 位用 `Long.*Unsigned`。
* 可以说出口的话：“32 个 bit 是一样的，只是怎么读不同。我用 int 存，在三个地方显式用无符号版本：右移、转 long、打印。”

**Q2：`x << 32` 在 Java 里是多少？C++ 呢？**

* 答案要点：Java 位数取低 5 位（`n & 31`），`x << 32 == x`；C++ 位数 ≥ 位宽是未定义行为。题面要的硬件语义是 0，所以要自己判断，或用 `long` 移位后截断。

**Q3：怎么数一个数里 1 的个数？**

* 答案要点：`Integer.bitCount`（编译成 `POPCNT` 指令）；手写 Kernighan：`while (x != 0) { x &= x - 1; count++; }`，每次清掉最低位的 1，循环次数 = 1 的个数；或 SWAR 并行加法。
* 可以说出口的话：“`x & (x-1)` 会把最低位的 1 清掉，因为 x−1 把最低位的 1 变 0、它右边的 0 全变 1，AND 之后这些位都是 0。”

**Q4：不借助临时变量，交换两个寄存器的值？**

* 答案要点：`a ^= b; b ^= a; a ^= b;`；若 `a` 和 `b` 是同一个变量会变成 0。

**Q5：性能还能怎么优化？**

* 答案要点：解码一次到 `int[]`（已做）；融合相邻的纯位运算为 `(r & a) ^ x`；常量折叠；生成字节码消除分发；批量不同初值可用向量化；诚实指出间接跳转 + 分支预测是随机程序上的剩余瓶颈（本机实测 1.5× vs 9×）。

**Q6：寄存器改成 64 位 / 可变位宽？**

* 答案要点：`long` + `Long.*Unsigned`；位宽 w < 64 时每次运算后 `& ((1L << w) - 1)`；w == 64 时 `1L << 64 == 1`（位数 mod 64），要特判；所有 `Integer.*` 换 `Long.*`。

**Q7：这个模拟器怎么测试？**

* 答案要点：每条指令的真值表；边界（0、全 1、最高位、位 0 / 位 31）；性质测试（`expand(compress(x,m),m) == x & m`、`reverse(reverse(x)) == x`、`parseValue(hex(x)) == unsigned(x)`）；用 `long` 写一份独立的参照实现随机对拍（本题 `matchesALongBasedOracle`）；编译版与解释版逐程序比较。

---

## 8. 常见误区

1. **`>>` 代替 `>>>`**——`0xF0000000 >> 4` 得 `0xFF000000`，高位被补了 1。寄存器该用 `>>>`（测试 `shiftsAreLogicalAndDropBits`）。
2. **`Integer.parseInt("FFFFFFFF", 16)`**——抛 `NumberFormatException`；`4294967295` 同样。要用 `Long.parseLong` 再 `(int)`（测试 `maskOperandsAreUnsigned32Bit`）。
3. **`reg << n` 当 `n ≥ 32`**——Java 位数 mod 32，`SHL 32` 保持原值；`SHL 33` 变成 `SHL 1`（测试 `shiftsOf32OrMoreClearTheRegister`）。
4. **`(long) reg` 想转无符号**——符号扩展，`-1` 变 `-1L`。正确是 `Integer.toUnsignedLong(reg)` 或 `reg & 0xFFFFFFFFL`。
5. **`1 << b` 里 `b` 可以是 32**——`1 << 32 == 1`，悄悄操作了第 0 位。记录构造器里要校验 `0..31`（测试 `recordsGuardTheirOwnInvariants`）。
6. **输出用 `Integer.toString`**——`0xFFFFFFFF` 打印 `-1`（测试 `unsignedInterpretation`）。
7. **`Long.decode("010")`**——前导 0 当八进制，得到 8（测试 `parseValueBases`）。
8. **`ROL 36` 不等于 `ROL 4`**——手写旋转没有对 32 取模（测试 `rotationsWrapAroundAndTakeModulo32`）。
9. **`numberOfTrailingZeros(0)` 当成 −1 或抛异常**——它返回 32（测试 `countingQueries`）。

---

## 9. 自测题

**题 1（概念）**：8 位的位模式 `1010 0110` 当有符号数是多少？当无符号数呢？

<details><summary>答案</summary>

无符号：128 + 32 + 4 + 2 = 166。有符号：−128 + 32 + 4 + 2 = −90（或 166 − 256 = −90）。
</details>

**题 2（手算）**：`x = 0xB6 = 1011 0110`。算 `x << 2`、`x >>> 2`、`x >> 2`（都当 8 位）。

<details><summary>答案</summary>

`x << 2 = 1101 1000`（高 2 位 `10` 丢弃，低位补 0）；`x >>> 2 = 0010 1101`；`x >> 2 = 1110 1101`（最高位是 1，补 1）。
</details>

**题 3（Java 行为）**：下面各表达式的值（`int`）？`1 << 32`；`-1 >>> 28`；`-1 >> 28`；`Integer.bitCount(-1)`；`Integer.numberOfLeadingZeros(0)`。

<details><summary>答案</summary>

`1 << 32 == 1`（位数 mod 32）；`-1 >>> 28 == 15`（`0xF`）；`-1 >> 28 == -1`（补 1）；`bitCount(-1) == 32`；`numberOfLeadingZeros(0) == 32`。
</details>

**题 4（小编程）**：写 `static boolean isPowerOfTwo(int x)`，把 `x` 当无符号数，判断是否恰好有一个 bit 是 1。不用循环。

<details><summary>答案</summary>

```java
static boolean isPowerOfTwo(int x) {
    return x != 0 && (x & (x - 1)) == 0;     // 或 Integer.bitCount(x) == 1
}
```

`x & (x-1)` 清掉最低位的 1；结果为 0 说明原来只有一个 1。`0x80000000`（负数）也返回 true，这是对的：它的位模式只有最高位是 1。
注意 `x != 0`：0 满足 `x & (x-1) == 0`（`0 & -1 == 0`），但 0 个 1 不是 2 的幂。
</details>

**题 5（设计）**：把 `RegisterSim` 扩展成 8 个寄存器 `R0..R7`，指令如 `AND R3 0xFF`。数据结构怎么设计？性能版本怎么改？

<details><summary>答案</summary>

加一层 `Operand`（`Reg(int index)` 或 `Imm(int value)`）；寄存器文件用 `int[8]`。性能版本里 `args` 变成两个数组（目标寄存器编号 + 操作数 / 源寄存器编号），热循环 `regs[dst] = regs[dst] & (isImm ? imm : regs[src])`：把“立即数还是寄存器”也在解码时分成不同的操作码，避免循环里再判断。
</details>

**题 6（实验）**：用 `jtest.py` 把参考实现的 `Shr` 分支从 `reg >>> n` 改成 `reg >> n`，预测哪个测试会失败。

<details><summary>答案</summary>

`shiftsAreLogicalAndDropBits`（`0x80000000 >>> 31` 变成 `-1`），并且 `matchesALongBasedOracle`、`compiledAgreesWithInterpreterOnSmallPrograms`（解释版与编译版出现差异）也会失败。
</details>

---

## 10. 延伸阅读

* Henry S. Warren, *Hacker's Delight*（第 2 版）第 2 章（基本位运算技巧）与第 5 章（计数 1 位）：popcount、`x & (x-1)`、旋转、翻转的经典来源。
* Bryant & O'Hallaron, *Computer Systems: A Programmer's Perspective*（CSAPP）第 2 章 2.1–2.3：信息的表示——补码、有符号 / 无符号转换、移位、整数运算，配大量例子。
* Java 语言规范 JLS §15.19「Shift Operators」：确认“位数只取低 5 位（int）/ 低 6 位（long）”。
* `java.lang.Integer` 的 Javadoc：`compress`、`expand`、`rotateLeft`、`reverse`、`reverseBytes`、`bitCount`、`toUnsignedString`、`compareUnsigned` 的精确定义。
* `java.util.HexFormat` 的 Javadoc：`toHexDigits` 的位数与大小写规则。
* JEP 441（switch 模式匹配）、JEP 440（record 模式）、JEP 409（sealed）：本题的数据建模语言基础。
* Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*，流水线与分支预测章节：为什么随机分支很贵。
