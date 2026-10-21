# hc06 · CPU 寄存器位运算 —— 讲义

> 读者：会写基本 Java，不懂二进制也没关系——第 2 节从「什么是 bit」讲起。

---

## 1. 这道题在问什么

CPU 里的**寄存器**（register）是小存储单元，32 位寄存器就是 **32 个开关**，每个开（1）或关（0）。题目给初值和一串指令（“关掉某几个开关”“整体左挪 4 格”“数有几个开着”……），依次执行并输出。

### 手算一遍

初值 `0xF0`（十六进制，十进制 240）。程序：

```
AND 0x3C
SHL 4
OR 0x0F
POPCOUNT      → 输出 1 的个数
NOT
SHR 28
POPCOUNT
```

写成二进制（只写低 12 位，高位全 0）：

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

难在**每步都有 Java 特有的坑**：`NOT` 之后 `int` 是**负数**；`SHR` 写成 `>>` 会补 1；`SHL 32` 不是 0……

---

## 2. 前置知识

### 2.1 二进制、bit、字节、十六进制

bit 只取 0 或 1，n 个 bit 表示 2ⁿ 个值，8 个 bit 是**字节**（byte）。按“位权”读：从右往左第 k 位权重 2ᵏ。

```
位号:     7    6    5    4    3    2    1    0
位权:   128   64   32   16    8    4    2    1
        0    0    1    0    1    1    0    1       = 32 + 8 + 4 + 1 = 45
```

32 位二进制太长；十六进制每位对应**恰好 4 个 bit**，32 位正好 8 个字符，逐位直接换算：

```
二进制  0000 0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111
十六进制  0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F

0xDEADBEEF = 1101 1110 1010 1101 1011 1110 1110 1111
              D    E    A    D    B    E    E    F
```

```java
int a = 0xFF;          // 十六进制字面量，255
int b = 0b1010;        // 二进制字面量，10
int c = 0xFFFFFFFF;    // 注意：这是个 int 字面量，值是 -1（见 2.2）
```

### 2.2 补码、有符号与无符号：同样 32 个 bit，两种读法

`int` 的 32 个 bit 要同时表示正负。**补码**（two's complement）：最高位（第 31 位）权重是**负的** −2³¹，其余照旧。8 位演示：

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

32 位同理：`0xFFFFFFFF` 有符号读 **−1**，无符号读 **4 294 967 295**；`0x80000000` 有符号 −2 147 483 648，无符号 2 147 483 648。

**对本题至关重要**：寄存器是**无符号 32 位**，Java **没有无符号 int**；但 bit 一样，只是“解释”不同。所以用 `int` 存位模式：位运算（`& | ^ ~ <<`）只看 bit，无区别；而**右移**、**比较大小**、**转十进制字符串 / `long`** 三类操作结果不同，必须显式选无符号版本。

```java
int reg = 0xFFFFFFFF;                        // 位模式全 1，值是 -1
long u = Integer.toUnsignedLong(reg);        // 4294967295L：先零扩展到 64 位
String s = Integer.toUnsignedString(reg);    // "4294967295"
Integer.compareUnsigned(0x80000000, 1) > 0;  // true：按无符号 2147483648 > 1
```

`(long) reg` 是**错的**——会符号扩展成 `-1L`。

### 2.3 位运算：AND、OR、XOR、NOT

对两个数的**每一位独立**做布尔运算：

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

`&` **关掉**不想要的开关、`|` **打开**、`^` **翻转**；`~reg` 翻转全部 32 位（`~0 == 0xFFFFFFFF == -1`）。

### 2.4 掩码（mask）与单个 bit 的操作

掩码是“选哪几位”的模板；操作第 b 位用掩码 `1 << b`。

| 操作 | 公式 | 为什么 |
|---|---|---|
| 置 1（SET） | `reg \| (1 << b)` | OR 1 一定是 1，其他位 OR 0 不变 |
| 清 0（CLEAR） | `reg & ~(1 << b)` | `~(1<<b)` 只有第 b 位是 0，AND 它只清第 b 位 |
| 翻转（TOGGLE） | `reg ^ (1 << b)` | XOR 1 翻转，XOR 0 不变 |
| 测试 | `(reg >>> b) & 1` | 把第 b 位挪到最低位再 AND 1 |

```
reg = 1011 0110 (8 位演示)，b = 3，1<<3 = 0000 1000
SET    reg | 0000 1000 = 1011 1110
CLEAR  reg & 1111 0111 = 1011 0110   （第 3 位本来就是 0，没变）
TOGGLE reg ^ 0000 1000 = 1011 1110
```

**坑**：`1 << 31` 在 `int` 里是负数，但位模式正是“只有最高位”，作掩码正确。位号必须 0..31：`1 << 32` 在 Java 里等于 `1`（2.5），位号 32 要在入口拒绝。

### 2.5 移位：`<<`、`>>`、`>>>`

整体向左或向右挪 n 格，挪出去的丢掉；空出来的格子补什么分三种：

```
8 位演示，x = 1011 0110 (0xB6)

x << 2   左移：低位补 0，高位挪出的丢掉         = 1101 1000   （最高 2 位 "10" 丢了）
x >>> 2  逻辑右移：高位补 0                     = 0010 1101
x >> 2   算术右移：高位补“原来的最高位”（符号位）= 1110 1101   （x 最高位是 1，补 1）
```

* `>>>`（逻辑右移）：永远补 0，**寄存器就该用这个**。
* `>>`（算术右移）：补符号位，用于有符号数除以 2ⁿ 保持符号。`0xF0000000 >> 4 = 0xFF000000`，**不是**要的 `0x0F000000`；最高位为 1 时（如 `NOT` 之后）会带进垃圾 1。

**Java 的特殊规则（重要）**：对 `int`，移位位数**只取低 5 位**，即 `n & 31`：

```java
int x = 0xFFFFFFFF;
x << 32    // == x << 0 == 0xFFFFFFFF，不是 0！
x << 33    // == x << 1
x >>> 32   // == x
```

C/C++ 里位数 ≥ 位宽是**未定义行为**。题目（硬件语义）要移 32 位或更多时 32 个 bit 全挤出去，结果 0。所以自己判断（`n >= 32 ? 0 : x << n`），或用 `long`（步骤 8）。

### 2.6 旋转（rotate）

像移位，但挪出去的 bit 从另一头**绕回来**，一个不丢。

```
x = 0x12345678 = 0001 0010 0011 0100 0101 0110 0111 1000
ROL 4（循环左移 4 位）：最高的 4 位 0001 绕到最低位
  = 0010 0011 0100 0101 0110 0111 1000 0001 = 0x23456781
ROR 4：最低的 4 位 1000 绕到最高位
  = 1000 0001 0010 0011 0100 0101 0110 0111 = 0x81234567
```

位数对 32 取模：`ROL 32` 不变，`ROL 36 == ROL 4`。`Integer.rotateLeft(x, n)` / `rotateRight` 已按 `n mod 32` 处理，是 JIT intrinsic（编译成一条旋转指令）。手写 `(x << n) | (x >>> (32 - n))` 在 `n == 0` 时 `x >>> 32 == x`，碰巧正确；换成 `>>` 就错。

### 2.7 计数与重排：popcount、ctz、clz、reverse、bswap、compress、expand

* **popcount**：数 1 的个数，`Integer.bitCount(x)`（CPU `POPCNT`）。`bitCount(0) == 0`，`bitCount(-1) == 32`。
* **ctz**（末尾 0 个数，即“最低的 1 在第几位”）：`Integer.numberOfTrailingZeros(x)`，`x == 0` 返回 **32**。
* **clz**（前导 0 个数）：`Integer.numberOfLeadingZeros(x)`，`x == 0` 为 32，`x < 0` 为 0。
* **reverse**：32 个 bit 整体倒过来，`Integer.reverse(1) == 0x80000000`。
* **bswap**（字节序翻转）：4 个字节倒序，字节内不变，`Integer.reverseBytes`：`0x12345678 → 0x78563412`（网络大小端互转）。
* **compress / expand**（Java 19 起）：按掩码收拢 / 散开。`compress(x, mask)` 取 x 中 mask 为 1 的位，**按顺序**挤到低位。

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

  `expand(v, mask)` 反过来：把 v 的低位依次放进 mask 为 1 的位置，其余补 0。性质 `expand(compress(x, m), m) == x & m`。x86 BMI2 的 `PEXT/PDEP` 一条指令完成，其他平台走软件实现。

### 2.8 字符串里的数怎么读：进制、范围、为什么用 long

输入可能是 `255`、`0xFF`、`0b11111111`：要按前缀定进制、检查字符、检查范围。

**不用 `Integer.parseInt`**：有符号 `int`，`parseInt("4294967295")` 和 `parseInt("FFFFFFFF", 16)` 都抛 `NumberFormatException`，却是 32 位寄存器的合法值。改用 `Long.parseLong(digits, radix)`，检查 `0 ≤ v ≤ 0xFFFFFFFFL`，最后 `(int) v`——只保留低 32 位，位模式不变。**也不用 `Long.decode`**：前导 0 当八进制（`"010"` 是 8），还接受 `-` 和 `#`。还要逐字符 `Character.digit(c, radix)` 检查，因为 `Long.parseLong` 接受 `+1`。

### 2.9 CPU 的分支预测与缓存（只为步骤 8）

**流水线**：CPU 同时处理十几条指令的不同阶段；遇到**分支**（`if`、`switch` 跳转）时不知走哪条路，就**猜**一个继续。**分支预测**：猜对白赚，猜错则已做一半的指令作废，代价约十几个周期。规律序列猜得准，随机序列几乎只能蒙。

**缓存**：读一个字节会顺便把附近一整行（通常 64 字节）拉进缓存。连续的 `int[]` 读完第 k 个，第 k+1..k+15 个已在缓存里；`Object[]` 存引用，对象散落堆上，读每个都可能再访问一次内存。

### 2.10 本题用到的 Java 语法

`record`、`sealed interface … permits`、`switch` 模式匹配（`case And(var m) -> …`）、`switch` 表达式、文本块、`HexFormat`（第 6 节）。

---

## 3. 从最笨的解法开始

大多数人：字符串比较指令名，`int` 存寄存器，`Integer.parseInt` 读数，`println` 输出。

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

复杂度 O(m)（m = 指令数），没问题。**这些输入上是错的**：

| 输入 | 期望 | 这份代码 | 原因 |
|---|---|---|---|
| 初值 `4294967295` | 合法 | 抛 `NumberFormatException` | `parseInt` 是有符号 int 范围（2.8） |
| `AND 0xFFFFFFFF` | 合法 | 抛异常，且不认 `0x` 前缀 | 同上 |
| 初值 `0x80000000`，`SHR 31` | 1 | `-1` | `>>` 补符号位（2.5） |
| 初值 `1`，`SHL 32` | 0 | 1 | 移位位数只取低 5 位（2.5） |
| 终值 `0xFFFFFFFF` | `4294967295` | `-1` | 没用无符号输出（2.2） |
| `SET 32` | `Malformed Input` | `1 << 32 == 1` 悄悄置了第 0 位 | 位号越界没检查 |
| 指令 `FOO` | `Malformed Input` | 默默忽略 | 没有 `else` |
| `ROL 36` | 同 `ROL 4` | 没实现 | |

**全部难度在边界**。

---

## 4. 一步一步改进

### 步骤 1：数字解析——用 `long`，严格校验

`parseInt` 读不了 32 位无符号数，也不认 `0x`、`0b`。自写 `parseValue`：识别前缀 → 逐字符检查 → `Long.parseLong` → 范围 `0..0xFFFFFFFFL` → 返回 `long`（强转 `(int)` 位模式不变）。**边界**：`"010"` 是十进制 10；单独的 `"0x"`、`"-1"`、`"+1"`、`"4294967296"` 非法。

### 步骤 2：把指令从“字符串”变成“类型”

字符串比较散落各处、每条都重新比较；拼写错误（`"ShR"`）编译器发现不了；非法指令（`SET 32`）到执行时才发现。每种指令一个 `record`，全部实现 sealed 接口 `Instr`，非法值在**构造时**被紧凑构造器拒绝：

  ```java
  public record SetBit(int bit) implements Update {
      public SetBit { if (bit < 0 || bit > 31) throw new IllegalArgumentException("bit out of 0..31: " + bit); }
  }
  ```

执行时对 sealed 接口写 `switch`，编译器检查每种指令都有分支：

  ```java
  case And(var m) -> reg & m;
  case Shl(var n) -> n >= 32 ? 0 : reg << n;
  ```

再拆一层：改寄存器的 `Update`，只读并输出一个数的 `Query`（`POPCOUNT` 等）。`apply` 返回新寄存器值，`query` 返回要输出的数，类型就说明“会不会改寄存器”。

### 步骤 3：无符号语义

* **`SHR`**：`reg >>> n`（2.5），不用 `>>`。
* **输出**：十进制 `Integer.toUnsignedString(reg)`；转 `long` 用 `Integer.toUnsignedLong(reg)`。
* **十六进制**：`HexFormat.of().withUpperCase().toHexDigits(reg)`——固定 8 字符、补零、按位模式（无负号），加前缀 `"0x"`。
* **二进制**：`Integer.toBinaryString(reg)` 不补前导零（5 → `"101"`），手动补到 32 位：`StringBuilder.repeat('0', 32 - raw.length())`。

### 步骤 4：移位位数 ≥ 32

`reg << 32 == reg`。简单做法 `n >= 32 ? 0 : reg << n`（有分支但清楚）；免分支见步骤 8。

### 步骤 5：旋转

`Integer.rotateLeft(reg, n)` / `rotateRight` 本就取 `n mod 32`（`ROL 36 == ROL 4`）。手写 `(reg << n) | (reg >>> (32 - n))` 也行，要意识到 `n % 32 == 0` 时是碰巧对。

### 步骤 6：整合输出与错误处理

`solve(lines)`：第一个有效行是初值，其余是程序；每个 Query 输出一行十进制，最后一行 `describe(终值)`（`hex dec bin`）。任何 `MalformedProgramException` → 只输出 `Malformed Input`；解析阶段捕获构造器抛的 `IllegalArgumentException` 并转成它。

### 步骤 7：扩展指令，别手写

`COMPRESS / EXPAND / REVERSE / BSWAP / CTZ / CLZ` 直接用 `Integer` 的对应方法（2.7）。`Instr` 是 sealed，新增这 6 个 record 后 `apply` 和 `query` 的 `switch` **立刻编译报错**，逼你补全——sealed 的价值。面试官看的是你知道标准库已有，不会写 20 行循环。

### 步骤 8：性能——解码一次，`int[]`，无分支

**问题**：1000 万条指令，或同一程序对大量初值各跑一遍。`run()` 每步取对象（指针追逐）、类型分派、record 解构。**想法**：**编译**一次，把程序变成两个 `int[]`：`ops[]`（操作码 0..13）和 `args[]`（操作数）；热循环只有数组读写和一个 `switch (ops[pc])`，不创建对象。

**解码时的化简**：
* `NOT` = `XOR 0xFFFFFFFF`；`SET b` = `OR (1<<b)`；`CLEAR b` = `AND ~(1<<b)`；`TOGGLE b` = `XOR (1<<b)`。操作码从 18 种降到 14 个。
* 移位位数 `Math.clamp(c, 0, 32)`；旋转位数 `c & 31`。

**移位免分支**：

  ```java
  case SHL -> reg = (int) (Integer.toUnsignedLong(reg) << a);   // a ∈ [0, 32]
  case SHR -> reg = (int) (Integer.toUnsignedLong(reg) >>> a);
  ```

`Integer.toUnsignedLong(reg)` 把 32 位零扩展到 64 位；`long` 移位位数最多 63，`<< 32` 真移 32 位：原来 32 个 bit 全推到高半部分，`(int)` 强转只留低 32 位，得 0。右移 32 同理。

**数据**（200 万条指令，预热后）：

| 程序形态 | `run`（对象 + 模式匹配） | `execute`（`int[]`） |
|---|---|---|
| 随机 18 种指令 | 21 ms | 14 ms |
| 随机，只含 14 种更新型指令 | 17 ms | 11 ms |
| 固定循环的 14 条指令（周期序列） | 9 ms | **1 ms** |

**解读**：规律序列快 9 倍，随机序列只快 1.5 倍：`switch` 是一条**间接跳转**，操作码随机时分支预测大量猜错（2.9），每次损失十几个周期。所以“无分支”指**指令语义内部**（移位、位号），不是分发。

**还能更快**（口头提）：把相邻的 `AND/OR/XOR/NOT/SET/CLEAR/TOGGLE` 融合成一条 `r = (r & a) ^ x`；常量折叠；整个程序编译成字节码让 JIT 去掉分发。

---

## 5. 逐段讲解法

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

* 两层 sealed：`Instr` 只能是 `Update` 或 `Query`；`Update` 只能是 15 个 record 之一，编译器逐层检查穷尽。`record Not()` 无字段，只表示“这是 NOT”。
* `public SetBit { … }` 紧凑构造器在字段赋值**之前**校验，非法的 `SetBit(32)` 构造不出来。
* 分 `Update`/`Query` 因“返回值含义”不同（新寄存器值 vs 要输出的数）。

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

* `t.length() > 2`：单独的 `"0x"` 不进前缀分支，按十进制解析，`'x'` 被拒。
* 逐字符检查为拒绝 `+1`、`-1`、`1_0`（`Long.parseLong` 本身接受 `+`/`-`）。
* 超过 `long` 时 `parseLong` 抛 `NumberFormatException`，转成 `MalformedProgramException`。

```java
return switch (p[0].toUpperCase(Locale.ROOT)) {
    case "AND" -> new And(mask(p));
    case "NOT" -> bare(p, new Not());
    case "SHL" -> new Shl(small(p));
    ...
    default -> throw new MalformedProgramException("unknown instruction: " + p[0]);
};
```

* `Locale.ROOT`：避免土耳其语环境下 `"i".toUpperCase()` 变成带点的 `İ`。
* `mask(p)` 读 `parseValue` 后 `(int)` 强转：`0xFFFFFFFF` 变 `And(-1)`，位模式全 1，正是想要的掩码。
* `small(p)` 读位数 / 位号：纯十进制，且须装进 `int`。

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

* 无 `default`：`Update` 是 sealed，编译器保证 15 种都覆盖。`case Not _` 的 `_` 表示不关心字段（Java 21 预览）。
* `n >= 32 ? 0 : …` 明确“≥ 32 得 0”；`Integer.rotateLeft` 对任意位数按 mod 32，`Rol(Integer.MAX_VALUE)` 也安全。

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

* `checkedInitial` 检查 `0 ≤ initial ≤ 0xFFFFFFFFL` 再 `(int)` 强转；初值用 `long` 传入因为 4294967295 放不进非负 `int`。
* 外层 `switch` 只有 `Update`、`Query` 两个分支（`Instr` 只 `permits` 这两个）；`List.copyOf` 给调用方不可变列表。

### 5.5 格式化

```java
public static String hex(int reg) { return "0x" + HexFormat.of().withUpperCase().toHexDigits(reg); }
public static String bin(int reg) {
    String raw = Integer.toBinaryString(reg);
    return new StringBuilder(32).repeat('0', 32 - raw.length()).append(raw).toString();
}
public static String dec(int reg) { return Integer.toUnsignedString(reg); }
```

* `HexFormat.toHexDigits(int)`：固定 8 位、补零、按位模式（`-1 → "FFFFFFFF"`）。
* `StringBuilder.repeat(char, int)`（Java 21）：旧写法 `"0".repeat(n)` 多建一个字符串。
* `Integer.toBinaryString(-1)` 本就是 32 个 `1`，补 0 个 `0`。

### 5.6 `compile` / `execute`

```java
public record Compiled(int[] ops, int[] args, int queryCount) {}

case Not _          -> { ops[k] = XOR; args[k] = -1; }
case SetBit(var b)  -> { ops[k] = OR;  args[k] = 1 << b; }
case Shl(var c)     -> { ops[k] = SHL; args[k] = Math.clamp(c, 0, 32); }
case Rol(var c)     -> { ops[k] = ROL; args[k] = c & 31; }
```

* 平行数组 `ops[k]`、`args[k]` 在内存里连续（缓存友好，2.9）。
* `Math.clamp(c, 0, 32)`（Java 21）把位数夹到 `[0, 32]`，旧写法 `Math.min(Math.max(c, 0), 32)`。
* `queryCount` 预先数好，一次分配输出数组，热循环不扩容。

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

* `int` 常量 `switch` 编译成 `tableswitch`（跳转表）；热循环里无 `new`、无类型检查。
* 返回时 `Arrays.stream(out).boxed().toList()` 装箱成 `List<Integer>`，只做一次，在循环外。

---

## 6. Java 21 特性小课

### record + 紧凑构造器

旧写法：每条指令一个带 `equals/hashCode/toString` 的 final 类，校验写在构造器。新写法 `record SetBit(int bit) { SetBit { checkBit(bit); } }`；`parseLine("AND 0xFF")` 可直接与 `new And(0xFF)` 比较。**不该用**：要继承其他类或需可变字段时。

### sealed、switch 模式匹配、switch 表达式

旧写法：`enum Op { AND, OR, … }` 加一堆可空字段，或 `interface Instr` 配 `instanceof` 链加最后 `else throw`。`sealed interface … permits …` 让编译器知道所有实现，`switch` 漏一种编译失败。`case And(var m) -> reg & m;` 一次完成“是不是 And”“取出 mask”，无强转。**别用 `default` 兜底**，否则编译器不再提醒你漏了新指令。`switch` 表达式每分支是值，无 `break`/fallthrough。

### 未命名模式 `_`（预览）

`case Not _ ->`、`case Popcount _ ->`：record 没有需要的字段，`_` 说明“不绑定”。需要 `--enable-preview`。

### 位运算与数学小工具

`Integer.compress/expand`（Java 19）、`rotateLeft`、`reverse`、`reverseBytes`、`bitCount`、`HexFormat`（Java 17）、`Integer.toUnsignedString`、`Math.clamp`（Java 21）、`StringBuilder.repeat`（Java 21）、`body.getFirst()` 代替 `body.get(0)`。旧写法都要手写循环或位技巧，易错且用不上 CPU 专用指令。

---

## 7. 追问预演

**Q1：Java 没有 unsigned int，怎么处理？**

* 要点：真正需要无符号的只有右移、比较、转十进制 / long。`int` 存位模式；右移 `>>>`；`Integer.toUnsignedLong` / `toUnsignedString` / `compareUnsigned`；64 位用 `Long.*Unsigned`。
* 说出口：“32 个 bit 一样，只是怎么读不同。我用 int 存，在三处显式用无符号版本：右移、转 long、打印。”

**Q2：`x << 32` 在 Java 里是多少？C++ 呢？**

* Java 位数取低 5 位（`n & 31`），`x << 32 == x`；C++ 位数 ≥ 位宽是未定义行为。题面硬件语义是 0，要自己判断，或用 `long` 移位后截断。

**Q3：怎么数 1 的个数？**

* `Integer.bitCount`（`POPCNT`）；手写 Kernighan：`while (x != 0) { x &= x - 1; count++; }`，循环次数 = 1 的个数；或 SWAR 并行加法。
* 说出口：“`x & (x-1)` 清掉最低位的 1：x−1 把它变 0、右边的 0 全变 1，AND 后这些位都是 0。”

**Q4：不用临时变量交换两个寄存器？**

* `a ^= b; b ^= a; a ^= b;`；若 `a` 和 `b` 是同一变量会变 0。

**Q5：性能还能怎么优化？**

* 解码一次到 `int[]`（已做）；融合相邻纯位运算为 `(r & a) ^ x`；常量折叠；生成字节码消除分发；批量初值可向量化；诚实指出间接跳转 + 分支预测是随机程序的剩余瓶颈（1.5× vs 9×）。

**Q6：寄存器改成 64 位 / 可变位宽？**

* `long` + `Long.*Unsigned`；位宽 w < 64 时每次运算后 `& ((1L << w) - 1)`；w == 64 时 `1L << 64 == 1`（mod 64）要特判；`Integer.*` 换 `Long.*`。

**Q7：怎么测试？**

* 每条指令真值表；边界（0、全 1、最高位、位 0 / 31）；性质（`expand(compress(x,m),m) == x & m`、`reverse(reverse(x)) == x`）；用 `long` 写独立参照实现随机对拍；编译版与解释版逐程序比较。

---

## 8. 常见误区

1. **`>>` 代替 `>>>`**——`0xF0000000 >> 4` 得 `0xFF000000`，高位被补 1。
2. **`Integer.parseInt("FFFFFFFF", 16)`**——抛 `NumberFormatException`，`4294967295` 同样。用 `Long.parseLong` 再 `(int)`。
3. **`reg << n` 当 `n ≥ 32`**——位数 mod 32，`SHL 32` 保持原值，`SHL 33` 变 `SHL 1`。
4. **`(long) reg` 想转无符号**——符号扩展，`-1` 变 `-1L`。用 `Integer.toUnsignedLong(reg)` 或 `reg & 0xFFFFFFFFL`。
5. **`1 << b` 里 `b` 可以是 32**——`1 << 32 == 1`，悄悄操作第 0 位。构造器里校验 `0..31`。
6. **输出用 `Integer.toString`**——`0xFFFFFFFF` 打印 `-1`。
7. **`Long.decode("010")`**——前导 0 当八进制，得 8。
8. **`ROL 36` 不等于 `ROL 4`**——手写旋转没对 32 取模。
9. **`numberOfTrailingZeros(0)` 当成 −1 或抛异常**——它返回 32。

---

## 9. 自测题

**题 1（概念）**：8 位位模式 `1010 0110` 当有符号数是多少？无符号呢？

<details><summary>答案</summary>

无符号：128 + 32 + 4 + 2 = 166。有符号：−128 + 32 + 4 + 2 = −90（166 − 256）。
</details>

**题 2（手算）**：`x = 0xB6 = 1011 0110`，算 `x << 2`、`x >>> 2`、`x >> 2`（都当 8 位）。

<details><summary>答案</summary>

`x << 2 = 1101 1000`（高 2 位 `10` 丢弃，低位补 0）；`x >>> 2 = 0010 1101`；`x >> 2 = 1110 1101`（最高位是 1，补 1）。
</details>

**题 3（Java 行为）**：`int` 表达式的值：`1 << 32`；`-1 >>> 28`；`-1 >> 28`；`Integer.bitCount(-1)`；`Integer.numberOfLeadingZeros(0)`。

<details><summary>答案</summary>

`1`（位数 mod 32）；`15`（`0xF`）；`-1`（补 1）；`32`；`32`。
</details>

**题 4（小编程）**：写 `static boolean isPowerOfTwo(int x)`，把 `x` 当无符号数，判断是否恰有一个 bit 为 1。不用循环。

<details><summary>答案</summary>

```java
static boolean isPowerOfTwo(int x) {
    return x != 0 && (x & (x - 1)) == 0;     // 或 Integer.bitCount(x) == 1
}
```

`x & (x-1)` 清掉最低位的 1，结果为 0 说明原来只有一个 1。`0x80000000`（负数）也返回 true：位模式只有最高位为 1。需要 `x != 0`：0 满足 `x & (x-1) == 0`，但 0 个 1 不是 2 的幂。
</details>

**题 5（设计）**：把 `RegisterSim` 扩展成 8 个寄存器 `R0..R7`，指令如 `AND R3 0xFF`。数据结构怎么设计？性能版本怎么改？

<details><summary>答案</summary>

加一层 `Operand`（`Reg(int index)` 或 `Imm(int value)`），寄存器文件用 `int[8]`。性能版本里 `args` 变成两个数组（目标寄存器 + 操作数 / 源寄存器），热循环 `regs[dst] = regs[dst] & (isImm ? imm : regs[src])`；把“立即数还是寄存器”也在解码时分成不同操作码，避免循环里再判断。
</details>

**题 6（实验）**：把 `SHR` 从 `reg >>> n` 改成 `reg >> n`，预测哪些输入出错。

<details><summary>答案</summary>

凡最高位为 1 的寄存器右移都会错：`0x80000000 >>> 31` 应得 1，却变成 `-1`。用 `long` 写的独立参照实现随机对拍，或把解释版与编译版逐程序比较，会立刻发现差异。
</details>

---

「延伸」Warren《Hacker's Delight》第 2、5 章（位运算技巧、计数 1 位）。
