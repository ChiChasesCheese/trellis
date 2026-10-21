# J15 · 数学与字符串小工具：溢出检测、`Math.clamp`、`HexFormat`、位操作

> 版本：`Math.*Exact` 8（`absExact` 15、`ceilDiv`/`floorDivExact` 等 18）· `String.formatted` 15 · `HexFormat` 17 · `Integer.compress/expand` 19 · **`Math.clamp`、`StringBuilder.repeat` 21**。全部正式特性。
> 可运行代码：`examples/J15/`。前置：`int`/`long` 的范围、二进制和十六进制；补码（two's complement）在 1.1 从零讲。

---

## 1. 先看痛点

### 1.1 从零讲：整数溢出是怎么回事

计算机里整数是固定宽度二进制：`int` 32 位，`long` 64 位，最高位当符号位（补码）。范围：

| 类型 | 最小 | 最大 |
|---|---|---|
| `int` | −2 147 483 648（约 −21 亿） | 2 147 483 647（约 21 亿） |
| `long` | −9 223 372 036 854 775 808 | 9 223 372 036 854 775 807（约 9.2×10¹⁸） |

超出范围**不会报错**，像里程表一样「绕回去」：`Integer.MAX_VALUE + 1` 变成 `Integer.MIN_VALUE`，叫**溢出**（overflow）。

交易里价格用「最小价位的整数倍」（tick）存成 `long`，数量也是 `long`，**名义金额 = 价格 × 数量**：价格 4×10⁹ tick、数量 3×10⁹ 就超过 9.2×10¹⁸。静默回绕的后果不是崩溃，而是**一个看起来正常的错误数字**，甚至负的成交额——最糟的 bug。

### 1.2 Java 8 的写法（`examples/J15/J15Old.java`）

```java
int px = 2_000_000_000, q = 2;
int notional = px * q;                                  // -294967296，没有任何异常

long a = Long.MAX_VALUE, b = 1, sum = a + b;
boolean overflow = ((a ^ sum) & (b ^ sum)) < 0;         // 手写溢出检测：符号位技巧，没人看得懂

StringBuilder sb = new StringBuilder();
for (int i = 0; i < 5; i++) sb.append('0');             // 手写循环拼 5 个 0
static int clamp(int v, int lo, int hi) { return Math.max(lo, Math.min(hi, v)); }   // 手写 clamp
String.format("%02x", b)                                // 手写 hex
```

输出：

```
px*q = -294967296   <- 悄悄变成负数，没有任何异常
long 相加溢出? true, sum = -9223372036854775808
00000 00000042 0a1bff
100 id=7 px=18950
```

---

## 2. 语法逐条讲

### 2.1 `Math.xxxExact`：溢出就抛 `ArithmeticException`

| 方法 | 含义 | 版本 |
|---|---|---|
| `addExact` / `subtractExact` / `multiplyExact` | 加 / 减 / 乘，`int` 与 `long` 重载（还有 `multiplyExact(long, int)`） | 8 |
| `incrementExact` / `decrementExact` / `negateExact` | +1 / −1 / 取负 | 8 |
| `toIntExact(long)` | `long` → `int`，放不下就抛 | 8 |
| `absExact` | 绝对值；`MIN_VALUE` 的绝对值放不下，抛异常 | 15 |
| `divideExact`、`floorDivExact`、`ceilDivExact` | 仅 `MIN_VALUE / -1` 会溢出 | 18 |

例 1 输出：

```
addExact(MAX, 1) -> ArithmeticException: long overflow
multiplyExact(4e9, 3e9) -> ArithmeticException: long overflow
toIntExact(3e9) -> ArithmeticException: integer overflow
negateExact(MIN) -> ArithmeticException: long overflow
absExact(MIN) -> ArithmeticException: Overflow to represent absolute value of Long.MIN_VALUE
Math.abs(Long.MIN_VALUE) = -9223372036854775808   <- 老 API 的陷阱
```

经典陷阱：`Math.abs(Long.MIN_VALUE)` **仍是负数**（+9.2×10¹⁸ 放不进 `long`）；`absExact` 才诚实。

### 2.2 整除的方向：`floorDiv`、`ceilDiv`、`floorMod`

Java 的 `/` 向 **0** 截断，`%` 的符号跟被除数，对负数很反直觉：

```
-7 / 2 = -3, floorDiv = -4, ceilDiv = -3
7 / 2  = 3, floorDiv = 3, ceilDiv = 4
-7 % 5 = -2, floorMod(-7, 5) = 3
```

* `Math.ceilDiv(a, b)`（18）：向上取整除法，**「需要几页/几批/几块」** 的标准写法：`Math.ceilDiv(103, 25) = 5`。旧写法 `(a + b - 1) / b` 在 `a` 接近 `MAX` 时自己溢出。
* `Math.floorMod(x, n)`：结果永远在 `[0, n)`。环形缓冲区、哈希桶下标用它，`x % n` 对负 `x` 会得到负下标。

### 2.3 `Math.clamp`（Java 21）

```java
Math.clamp(150, 0, 100)    // 100
Math.clamp(-5, 0, 100)     // 0
int shift = Math.clamp(40L, 0, 32);   // (long value, int min, int max) 重载返回 int
Math.clamp(3.7, 0.0, 1.0)  // 1.0
```

四个重载：`(long, int, int) -> int`、`(long, long, long) -> long`、`(double, double, double)`、`(float, float, float)`。`min > max` 抛 `IllegalArgumentException`；旧的手写 `Math.max(lo, Math.min(hi, v))` 在 `lo > hi` 时**悄悄返回 `lo`**，掩盖参数写反的 bug。

### 2.4 `String.formatted`（15）与 `StringBuilder.repeat`（21）

```java
"TRADE taker=%d maker=%d px=%d qty=%d".formatted(3, 1, 18950, 100)   // 等价于 String.format(同样的串, 参数...)

new StringBuilder().repeat('0', 32 - bin.length()).append(bin)       // repeat(int codePoint, int count)
new StringBuilder().repeat("ab", 3)                                   // repeat(CharSequence, int count) -> "ababab"
```

`formatted` 是**实例方法**，能直接接在文本块后面。`repeat` 的第一个形参是 `int` **码点**（code point），写 `'0'` 时 char 自动提升。`String.repeat(int)`（11）早有，`StringBuilder.repeat` 21 才补上，用于不想先建临时 String 时。

### 2.5 `HexFormat`（Java 17）

```java
HexFormat hf = HexFormat.of();
hf.formatHex(bytes)                                  // "0a1bff"
hf.withUpperCase().formatHex(bytes)                  // "0A1BFF"
HexFormat.ofDelimiter(":").withPrefix("0x").formatHex(bytes)   // "0x0a:0x1b:0xff"
hf.parseHex("0a1bff")                                // byte[] {10, 27, -1}
hf.withUpperCase().toHexDigits(48879)                // "0000BEEF"  固定 8 位，自动补零
HexFormat.fromHexDigits("ff")                        // 255
```

`toHexDigits(int)` 总输出**完整宽度**（int 8 位、long 16 位），不用手写 `%08x`；`Integer.toHexString` 不补零。

### 2.6 `Integer.compress` / `Integer.expand`（Java 19，`Long` 同名）

给一个**掩码** `mask`：

* `compress(v, mask)`：把 `v` 中 `mask` 为 1 的那些位**抽出来，靠右紧挨着排好**；
* `expand(v, mask)`：反过来，把 `v` 的低位依次**撒到 `mask` 为 1 的位置**。

```
v    = 1011 0110
mask = 1111 0000
compress(v, mask) = 1011          (取出高 4 位，靠右)
expand(0b1011, mask) = 1011 0000  (撒回高 4 位)
```

这是「位域打包」的原语：把分散的有用位拼成连续一串。例 3 用它把 8 字节股票代码压成 40 位。支持 BMI2 的 x86 上 JIT 可能把它们编译成单条 `PEXT`/`PDEP` 指令（面试说"可能被内联为一条指令"即可）。

---

## 3. 编译器和 JVM 到底做了什么

* **`Math.addExact` 等不是普通方法调用**。源码实现是「做加法，用符号位技巧判溢出，溢出就抛」，但 HotSpot C2 把它们当**内联函数**（intrinsic）：生成「加法指令 + 检查 CPU 溢出标志位 + 条件跳转到抛异常的冷路径」，无溢出时只比 `+` 多一条几乎不跳的分支。**别因怕慢而不用 Exact**，热路径也一样。
* **`Math.clamp`、`HexFormat`、`StringBuilder.repeat`**：纯库方法，无 JIT 魔法，无新语法。
* **陷阱：Exact 只保护它自己那一次运算。**

```java
int a = 2_000_000_000, b = 2;
long wrong = a * b;                 // 先按 int 相乘（已经溢出了），再扩展成 long
long right = (long) a * b;          // 先扩展再乘
long safe  = Math.multiplyExact((long) a, b);   // 想要溢出检测就用这个
```

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——Exact、整除方向、clamp（`J15Ex1.java`）

见 2.1–2.3，输出：

```
addExact(MAX, 1) -> ArithmeticException: long overflow
...
-7 / 2 = -3, floorDiv = -4, ceilDiv = -3
7 / 2  = 3, floorDiv = 3, ceilDiv = 4
-7 % 5 = -2, floorMod(-7, 5) = 3
103 条记录每页 25 条 -> 页数 = 5
clamp(150, 0, 100) = 100
clamp(-5, 0, 100)  = 0
clamp(40L, 0, 32)  = 32
clamp(3.7, 0.0, 1.0) = 1.0
min > max -> IllegalArgumentException
```

### 例 2：进阶——字符串工具箱（`J15Ex2.java`）

```
TRADE taker=3 maker=1 px=18950 qty=100
symbol: AAPL
vwap  : 189.57
00000000000000000000000000000101
ababab|-----
==========
[hi]  <- strip 会去掉 Unicode 空白；trim 不会去全角空格: [　hi]
isBlank: true / isEmpty: false
lines: [a, b, c]
formatHex           = 0a1bff
withUpperCase       = 0A1BFF
delimiter+prefix    = 0x0a:0x1b:0xff
parseHex("0a1bff")  = [10, 27, -1]
toHexDigits(int)    = 0000BEEF  (固定 8 位，自动补零)
toHexDigits(long)   = 00000000000000ff
fromHexDigits("ff") = 255
```

要点：`strip()`（11）按 Unicode 空白去，`trim()` 只去 ≤ U+0020 的字符，所以去不掉全角空格（最后的 `[　hi]` 里还留着）；`lines()` 同时处理 `\n` 和 `\r\n`；`parseHex` 返回的 `byte` 是**有符号**的，`0xff` 读出来是 `-1`。

### 例 3：贴近真实——位压缩股票代码（`J15Ex3.java`）

行情报文里代码是 8 字节、右补空格（`"AAPL    "`）。大写字母 `A..Z` 的 ASCII 是 `0x41..0x5A`，低 5 位恰是 1..26；空格 `0x20` 低 5 位是 0。所以：

```java
static final long KEEP_LOW5 = 0x1F1F1F1F1F1F1F1FL;
static long pack(String t8) { ... return Long.compress(word, KEEP_LOW5); }     // 8 字节 -> 40 位
static String unpack(long key) { long spread = Long.expand(key, KEEP_LOW5); ... }
```

输出：

```
key = 0x860c00000 (36 位有效), unpack = AAPL
MSFT -> MSFT
compress(10110110, 11110000) = 1011
expand(1011, 11110000) = 10110000
bitCount(0b10110110) = 5
numberOfTrailingZeros(0) = 32   <- 约定：0 返回 32，不是 -1
highestOneBit(100) = 64
rotateLeft(0x80000001, 1) = 0x3
reverseBytes(0x01020304) = 0x4030201
```

手算核对：`A`=00001、`A`=00001、`P`=10000、`L`=01100，后面 4 个空格各 00000，共 8×5 = 40 位：`00001 00001 10000 01100 0000…0`。最高 4 位是前导 0，`Long.toHexString` 不显示前导零，所以打印出 9 位十六进制 `860c00000`（数值位长 36）；完整 40 位字段是 `0x0860C00000`。`numberOfTrailingZeros(0)` 是 32（int 位宽）。

---

## 5. 坑与限制

### 5.1 中间量溢出 ≠ 结果溢出

`Math.addExact(a, b)` 在 `a + b` 超出时抛异常，**即便最终结果（后面还要减回去）能装下**。例：求 `Long.MIN_VALUE..Long.MAX_VALUE` 的和，结果恰是合法的 `Long.MIN_VALUE`，但中间量 `a+b` 或 `count` 会溢出。应对：捕获 `ArithmeticException`，退到 `BigInteger` 算精确值再判断能否装下。**抛异常不等于「错」，只是「这条快路径不能下结论」。**

### 5.2 Exact 的"异常"是行为，不是日志

热路径上每次溢出抛一次异常，成本大（构造栈），所以适合「溢出就是 bug / 非法输入」。需要**饱和**（saturate，超出取边界）时用 `clamp` 或手写。

### 5.3 没有的 Exact 方法

没有 `powExact`、`sumExact`（数组求和）、`squareExact`。数组求和要自己循环里用 `addExact`。

### 5.4 `clamp` 参数顺序是 `(value, min, max)`，不是 `(min, max, value)`

`(long, int, int)` 重载返回 `int`：`Math.clamp(c, 0, 32)`（`c` 是 `int`）给 `int`，直接当移位量用；要 `long` 就传三个 `long`。

### 5.5 `String.format`/`formatted` 的坑

* 默认用**当前 Locale**：德国 Locale 下 `%.2f` 输出 `189,57`。要稳定输出用 `String.format(Locale.ROOT, ...)`（`formatted` 没有带 Locale 的版本）。
* 钱不要用 `double`：存储与计算用 `long` 最小单位或 `BigDecimal`。
* `%d` 不接受 `double`，抛 `IllegalFormatConversionException`。

### 5.6 `repeat` 的参数

`"x".repeat(-1)`、`sb.repeat('0', -1)` 抛 `IllegalArgumentException`。补零宽度算出负数（已比目标宽）会炸，先 `Math.max(0, ...)`。

### 5.7 `HexFormat.parseHex` 要求偶数个字符且无分隔

用了 `withDelimiter` 的格式，`parseHex` 也必须用同一个 `HexFormat` 对象解。

### 5.8 `compress/expand` 的语义容易记反

`compress` = 分散 → 紧凑（抽取），`expand` = 紧凑 → 分散（还原），同一 mask 下互逆（对 `mask` 之内的位）。

---

## 6. 真实代码里的数学与位工具

* `OrderBook`：`// 先算后改：addExact 抛异常时下面还没有任何修改，簿保持原样` `long newTotal = Math.addExact(level == null ? 0L : level.total, qty);` —— 2.1。**异常安全**：先算出新值（可能抛）再改状态，溢出后订单簿不会停在一半修改的状态。
* `BatchMatcher`：`notional = Math.addExact(notional, Math.multiplyExact(t.price(), t.qty()));` —— 价格×数量溢出。
* `OrderBook`：`"TRADE taker=%d maker=%d side=%s px=%d qty=%d".formatted(taker, maker, side, px, q)` —— 2.4。
* `RecursiveSum`：`Math.addExact`、`Math.toIntExact(s)`、`Math.multiplyExact(count / 2, s)`、`Math.subtractExact(b, a)` —— 5.1 的中间量溢出（先除 2 再乘，少一次溢出机会）；`Math.ceilDiv((long) data.length, chunks)` —— 数组分块。
* 三个 ticker map：`values[index] = Math.addExact(values[index], delta);` —— 累加器溢出要报错。
* `RegisterSim`：`"0x" + HexFormat.of().withUpperCase().toHexDigits(reg)`（32 位寄存器固定 8 位大写 hex）；`new StringBuilder(32).repeat('0', 32 - raw.length()).append(raw).toString();`（二进制补前导零，`Integer.toBinaryString` 不补零）；`Integer.compress(reg, m)` / `Integer.expand(reg, m)`（题目就是模拟这条 CPU 指令）；`args[k] = Math.clamp(c, 0, 32);`（移位量限制到 0..32）；`Integer.bitCount(reg)`、`numberOfTrailingZeros(reg)`、`numberOfLeadingZeros(reg)`（对 0 的约定是 32）。
* `TickerCodec`：`return Long.compress(word, COMPRESS_MASK);` —— 例 3 的原型，`COMPRESS_MASK = 0x1F1F1F1F1F1F1F1FL`。
* `TickBook`：`return (w << 6) + Long.numberOfTrailingZeros(word);` —— 位图里找最低置位。
* `LongTickerMap`：`shift = 64 - Integer.numberOfTrailingZeros(capacity);` —— 容量是 2 的幂时 `numberOfTrailingZeros` 就是 log₂。

---

## 7. 自测题

1. `int a = 2_000_000_000; long x = a * 2;` 得到什么？怎么写才对？
2. `Math.abs(Integer.MIN_VALUE)` 的结果是什么？为什么？用哪个方法才能暴露问题？
3. `-7 / 2`、`Math.floorDiv(-7, 2)`、`Math.ceilDiv(-7, 2)`、`-7 % 5`、`Math.floorMod(-7, 5)` 各是多少？
4. 写出 `Integer.compress(0b1011_0110, 0b1111_0000)` 的二进制结果，并说明 `compress` 与 `expand` 的关系。
5. 为什么订单簿要「先 `addExact` 算出 `newTotal`，再修改状态」，而不是边改边算？

<details><summary>答案</summary>

1. `-294967296`：`a * 2` 先按 `int` 乘（溢出）再扩展。写 `Math.multiplyExact((long) a, 2)` 或 `(long) a * 2`；要检测溢出就用 Exact。
2. `Integer.MIN_VALUE`（仍是负数），+2 147 483 648 超出 `int` 最大值。`Math.absExact` 会抛 `ArithmeticException`。
3. `-3`、`-4`、`-3`、`-2`、`3`。
4. `1011`。`compress` 把 mask 为 1 的位抽出靠右排；`expand` 把紧凑的位撒回 mask 的 1 位置，在 mask 范围内互逆。
5. 异常安全（强保证）：`addExact` 抛异常时状态还没改，簿保持原样；边改边算则抛异常时可能已改了一半（如已扣队列但价位总量没更新），簿内部不一致。

</details>

---

「延伸」J16 并发原语：`VarHandle`、`Lock`、`Atomic*` 等。
