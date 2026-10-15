# J15 · 数学与字符串小工具：溢出检测、`Math.clamp`、`HexFormat`、位操作

> 版本：`Math.*Exact` 8（`absExact` 15、`ceilDiv`/`floorDivExact` 等 18）· `String.formatted` 15 · `HexFormat` 17 · `Integer.compress/expand` 19 · **`Math.clamp`、`StringBuilder.repeat` 21**。全部是正式特性，没有预览。
> 本课代码在 `study/10-java21/examples/J15/`，输出是本机 JDK 21.0.12 实跑的。
> 前置知识：`int`/`long` 的范围、二进制和十六进制的基本概念。补码（two's complement）第 1.1 节从零讲。
> 官方出处：`java.lang.Math` Javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html

---

## 1. 先看痛点

### 1.1 从零讲：整数溢出是怎么回事

计算机里整数是固定宽度的二进制。`int` 32 位，`long` 64 位，最高位当符号位（补码，two's complement）。范围：

| 类型 | 最小 | 最大 |
|---|---|---|
| `int` | −2 147 483 648（约 −21 亿） | 2 147 483 647（约 21 亿） |
| `long` | −9 223 372 036 854 775 808 | 9 223 372 036 854 775 807（约 9.2×10¹⁸） |

超出范围**不会报错**，而是像里程表一样「绕回去」：`Integer.MAX_VALUE + 1` 变成 `Integer.MIN_VALUE`。这叫**溢出**（overflow）。

交易里为什么要管：价格用「最小价位的整数倍」（tick）存成 `long`，数量也是 `long`；**名义金额 = 价格 × 数量**。价格 4×10⁹ tick、数量 3×10⁹ 就已经超过 9.2×10¹⁸。
静默回绕的后果不是崩溃，而是**一个看起来正常的错误数字**，甚至是负的成交额，这是最糟的 bug。

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

实测输出：

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

例 1 实测：

```
addExact(MAX, 1) -> ArithmeticException: long overflow
multiplyExact(4e9, 3e9) -> ArithmeticException: long overflow
toIntExact(3e9) -> ArithmeticException: integer overflow
negateExact(MIN) -> ArithmeticException: long overflow
absExact(MIN) -> ArithmeticException: Overflow to represent absolute value of Long.MIN_VALUE
Math.abs(Long.MIN_VALUE) = -9223372036854775808   <- 老 API 的陷阱
```

最后一行是个经典陷阱：`Math.abs(Long.MIN_VALUE)` 返回的**仍然是负数**，因为 +9.2×10¹⁸ 放不进 `long`。`absExact` 才是诚实的。

### 2.2 整除的方向：`floorDiv`、`ceilDiv`、`floorMod`

Java 的 `/` 向 **0** 截断，`%` 的符号跟着被除数。对负数这很反直觉：

```
-7 / 2 = -3, floorDiv = -4, ceilDiv = -3
7 / 2  = 3, floorDiv = 3, ceilDiv = 4
-7 % 5 = -2, floorMod(-7, 5) = 3
```

* `Math.ceilDiv(a, b)`（18）：向上取整除法。**「需要几页/几批/几块」** 的标准写法：`Math.ceilDiv(103, 25) = 5`。以前要写 `(a + b - 1) / b`，而它在 `a` 接近 `MAX` 时自己溢出。
* `Math.floorMod(x, n)`：结果永远在 `[0, n)`。做环形缓冲区下标、哈希桶下标时，`x % n` 对负 `x` 会得到负下标。

### 2.3 `Math.clamp`（Java 21）

```java
Math.clamp(150, 0, 100)    // 100
Math.clamp(-5, 0, 100)     // 0
int shift = Math.clamp(40L, 0, 32);   // (long value, int min, int max) 重载返回 int
Math.clamp(3.7, 0.0, 1.0)  // 1.0
```

四个重载：`(long, int, int) -> int`、`(long, long, long) -> long`、`(double, double, double)`、`(float, float, float)`。
`min > max` 抛 `IllegalArgumentException`（实测）。旧的手写 `Math.max(lo, Math.min(hi, v))` 在 `lo > hi` 时**悄悄返回 `lo`**，掩盖了参数写反的 bug。

### 2.4 `String.formatted`（15）与 `StringBuilder.repeat`（21）

```java
"TRADE taker=%d maker=%d px=%d qty=%d".formatted(3, 1, 18950, 100)   // 等价于 String.format(同样的串, 参数...)

new StringBuilder().repeat('0', 32 - bin.length()).append(bin)       // repeat(int codePoint, int count)
new StringBuilder().repeat("ab", 3)                                   // repeat(CharSequence, int count) -> "ababab"
```

`formatted` 是**实例方法**，所以能直接接在文本块（J07）后面。`repeat` 的第一个形参是 `int` 型的**码点**（code point），写 `'0'` 时 char 自动提升为 int。
`String.repeat(int)`（Java 11）早就有，`StringBuilder.repeat` 21 才补上，用于「不想先建一个临时 String」的场合。

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

`toHexDigits(int)` 总是输出**完整宽度**（int 8 位、long 16 位），不用再手写 `%08x`；`Integer.toHexString` 不补零（`RegisterSim.hex` 需要固定 8 位大写，用 `HexFormat` 一行解决）。

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

这是「位域打包」的一条原语：把分散在各处的有用位拼成连续一串。例 3 就用它把 8 字节的股票代码压成 40 位。在支持 BMI2 的 x86 CPU 上，
JIT 可以把它们编译成单条 `PEXT`/`PDEP` 指令（这是 JDK 内部的优化，我没有在本机验证，面试说“可能被内联为一条指令”即可）。

---

## 3. 编译器和 JVM 到底做了什么

* **`Math.addExact` 等不是普通 Java 方法调用**。Java 源码里它们的实现是「做加法，用符号位技巧判断溢出，溢出就抛」；但 HotSpot 的 C2 编译器把它们当作**内联函数**（intrinsic）：
  生成「加法指令 + 检查 CPU 的溢出标志位 + 条件跳转到抛异常的冷路径」。没有溢出时的代价只比 `+` 多一条几乎永远不跳的分支。**所以不要因为「怕慢」而不用 Exact**，热路径上也一样。
* **`Math.clamp`、`HexFormat`、`StringBuilder.repeat`**：纯库方法，没有 JIT 魔法，也没有新语法。
* **编译器层面的陷阱：Exact 只保护它自己那一次运算。**

```java
int a = 2_000_000_000, b = 2;
long wrong = a * b;                 // 先按 int 相乘（已经溢出了），再扩展成 long
long right = (long) a * b;          // 先扩展再乘
long safe  = Math.multiplyExact((long) a, b);   // 想要溢出检测就用这个
```

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——Exact、整除方向、clamp（`J15Ex1.java`）

见 2.1–2.3，完整实测输出：

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

要点：`strip()`（11）按 Unicode 空白去，`trim()` 只去 ≤ U+0020 的字符，所以全角空格 `　` 它去不掉（实测最后的 `[　hi]` 里还留着）；`lines()` 能同时处理 `\n` 和 `\r\n`；
`parseHex` 返回的 `byte` 是**有符号**的，`0xff` 读出来是 `-1`。

### 例 3：贴近真实——位压缩股票代码（`J15Ex3.java`）

行情报文里代码是 8 字节、右补空格（`"AAPL    "`）。大写字母 `A..Z` 的 ASCII 是 `0x41..0x5A`，低 5 位恰好是 1..26；空格 `0x20` 的低 5 位是 0。所以：

```java
static final long KEEP_LOW5 = 0x1F1F1F1F1F1F1F1FL;
static long pack(String t8) { ... return Long.compress(word, KEEP_LOW5); }     // 8 字节 -> 40 位
static String unpack(long key) { long spread = Long.expand(key, KEEP_LOW5); ... }
```

实测输出：

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

手算核对：`A`=00001、`A`=00001、`P`=10000、`L`=01100，后面 4 个空格各是 00000，共 8×5 = 40 位：`00001 00001 10000 01100 0000…0`。
最高的 4 位是前导 0，`Long.toHexString` 不显示前导零，所以打印出 9 位十六进制 `860c00000`（数值的位长是 36）。完整 40 位字段是 `0x0860C00000`。
`numberOfTrailingZeros(0)` 是 32（int 位宽）；`RegisterSim.java:206` 的注释专门写了这个约定。

---

## 5. 坑与限制

### 5.1 中间量溢出 ≠ 结果溢出

`Math.addExact(a, b)` 在 `a + b` 超出时抛异常，**即便最终结果（后面还要减回去）是能装下的**。`RecursiveSum.rangeSum` 的注释写得清楚：求 `Long.MIN_VALUE..Long.MAX_VALUE` 的和，结果恰好是 `Long.MIN_VALUE`，是合法的，但中间量 `a+b` 或 `count` 会溢出。
应对：捕获 `ArithmeticException`，退到 `BigInteger` 重新算精确值，再判断能不能装下。**抛异常不等于「错」，只是「这条快路径不能下结论」**。

### 5.2 Exact 的“异常”是行为，不是日志

热路径上溢出一次抛一次异常，成本很大（构造栈）。所以它适合「溢出就是 bug / 非法输入」的场景。需要**饱和**（saturate，超出就取边界）时别用 Exact，用 `clamp` 或手写。

### 5.3 没有的 Exact 方法

没有 `powExact`、`sumExact`（数组求和）、`squareExact`。数组求和要自己循环里用 `addExact`。

### 5.4 `clamp` 参数顺序是 `(value, min, max)`，不是 `(min, max, value)`

而且 `(long, int, int)` 重载返回 `int`：`Math.clamp(c, 0, 32)`（`c` 是 `int`）给你 `int`，直接当移位量用。如果你要 `long`，传三个 `long`。

### 5.5 `String.format`/`formatted` 的坑

* 默认用**当前 Locale**：德国 Locale 下 `%.2f` 会输出 `189,57`。要稳定输出用 `String.format(Locale.ROOT, ...)`（`formatted` 没有带 Locale 的版本，用 `String.format(Locale.ROOT, ...)`）。
* 钱不要用 `double`：`%.2f` 打印没问题，但存储与计算用 `long` 最小单位或 `BigDecimal`（kit 约定，见 CONVENTIONS.md）。
* `%d` 不接受 `double`，会抛 `IllegalFormatConversionException`。

### 5.6 `repeat` 的参数

`"x".repeat(-1)`、`sb.repeat('0', -1)` 抛 `IllegalArgumentException`。补零宽度算出负数（如已经比目标宽）会炸，要先 `Math.max(0, ...)`。

### 5.7 `HexFormat.parseHex` 要求偶数个字符且无分隔

用了 `withDelimiter` 的格式，`parseHex` 也必须用同一个 `HexFormat` 对象去解。

### 5.8 `compress/expand` 的语义容易记反

记住：`compress` = 从分散到紧凑（抽取），`expand` = 从紧凑到分散（还原）。两者在同一个 mask 下互逆（对 `mask` 之内的位）。

---

## 6. 在本 kit 哪里用到

| 文件与行 | 片段 | 对应 |
|---|---|---|
| `loop/rounds/01_video/hc05_market_order_book/reference/OrderBook.java:106-107, 141` | `// 先算后改：addExact 抛异常时下面还没有任何修改，簿保持原样` `long newTotal = Math.addExact(level == null ? 0L : level.total, qty);` | 2.1。**异常安全**：先算出新值（可能抛），再修改状态。保证溢出后订单簿不处于一半修改的状态 |
| `loop/rounds/01_video/hc05_market_order_book/reference/BatchMatcher.java:44-45` | `notional = Math.addExact(notional, Math.multiplyExact(t.price(), t.qty()));` | 2.1，1.1 的价格×数量溢出 |
| `loop/rounds/01_video/hc05_market_order_book/reference/OrderBook.java:337-341` | `"TRADE taker=%d maker=%d side=%s px=%d qty=%d".formatted(taker, maker, side, px, q)` | 2.4 |
| `loop/rounds/01_video/hc03_recursive_sum/reference/RecursiveSum.java:33-35, 190-192` | `Math.addExact`、`Math.toIntExact(s)`、`Math.multiplyExact(count / 2, s)`、`Math.subtractExact(b, a)` | 2.1；5.1 的中间量溢出（先除 2 再乘，少一次溢出机会） |
| `loop/rounds/01_video/hc03_recursive_sum/reference/RecursiveSum.java:279` | `Math.ceilDiv((long) data.length, chunks)` | 2.2：数组分块，`n` 个元素分 `k` 块，每块多大 |
| `loop/rounds/01_video/hc07_ticker_hash_map/reference/FrozenTickerMap.java:48`；`LongTickerMap.java:89`；`OffHeapTickerMap.java:97` | `values[index] = Math.addExact(values[index], delta);` | 2.1：累加器值溢出要报错 |
| `loop/rounds/01_video/hc06_cpu_register_bitwise/reference/RegisterSim.java:243` | `"0x" + HexFormat.of().withUpperCase().toHexDigits(reg)` | 2.5：32 位寄存器固定 8 位大写 hex |
| `RegisterSim.java:249` | `new StringBuilder(32).repeat('0', 32 - raw.length()).append(raw).toString();` | 2.4：二进制补前导零（`Integer.toBinaryString` 不补零） |
| `RegisterSim.java:199-200, 337-338` | `Integer.compress(reg, m)` / `Integer.expand(reg, m)` | 2.6：题目就是模拟这条 CPU 指令 |
| `RegisterSim.java:294-295` | `args[k] = Math.clamp(c, 0, 32);` | 2.3：移位量限制到 0..32 |
| `RegisterSim.java:206-211` | `Integer.bitCount(reg)`、`numberOfTrailingZeros(reg)`、`numberOfLeadingZeros(reg)` | 例 3；对 0 的约定是 32 |
| `loop/rounds/01_video/hc07_ticker_hash_map/reference/TickerCodec.java:78-97` | `return Long.compress(word, COMPRESS_MASK);` | 例 3：这就是本课例 3 的原型，`COMPRESS_MASK = 0x1F1F1F1F1F1F1F1FL` |
| `loop/rounds/01_video/hc05_market_order_book/reference/TickBook.java:182` | `return (w << 6) + Long.numberOfTrailingZeros(word);` | 位图里找最低置位 |
| `loop/rounds/01_video/hc07_ticker_hash_map/reference/LongTickerMap.java:38` | `shift = 64 - Integer.numberOfTrailingZeros(capacity);` | 容量是 2 的幂时，`numberOfTrailingZeros` 就是 log₂ |

---

## 7. 自测题

1. `int a = 2_000_000_000; long x = a * 2;` 得到什么？怎么写才对？
2. `Math.abs(Integer.MIN_VALUE)` 的结果是什么？为什么？用哪个方法才能暴露问题？
3. `-7 / 2`、`Math.floorDiv(-7, 2)`、`Math.ceilDiv(-7, 2)`、`-7 % 5`、`Math.floorMod(-7, 5)` 各是多少？
4. 写出 `Integer.compress(0b1011_0110, 0b1111_0000)` 的二进制结果，并说明 `compress` 与 `expand` 的关系。
5. 为什么 `hc05` 的 `OrderBook` 要「先 `addExact` 算出 `newTotal`，再修改状态」，而不是边改边算？

<details><summary>答案</summary>

1. `-294967296`，因为 `a * 2` 先按 `int` 乘（溢出）再扩展。写 `Math.multiplyExact((long) a, 2)` 或 `(long) a * 2`；想检测溢出就用 Exact。
2. `Integer.MIN_VALUE`（仍是负数）。因为 +2 147 483 648 超出 `int` 最大值。`Math.absExact` 会抛 `ArithmeticException`。
3. `-3`、`-4`、`-3`、`-2`、`3`。
4. `1011`。`compress` 把 mask 为 1 的位抽出来靠右排；`expand` 把紧凑的位撒回 mask 的 1 位置，两者互逆（在 mask 范围内）。
5. 异常安全（强保证）：`addExact` 抛异常时状态还没改，订单簿保持原样；如果边改边算，抛异常时可能已经改了一半（如已经扣了队列但价位总量没更新），簿内部就不一致了。

</details>

---

## 8. 延伸阅读

* `java.lang.Math` Javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html —— `clamp`、`ceilDiv`、各 Exact 的精确语义。
* `java.util.HexFormat` Javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HexFormat.html —— 分隔符、前后缀、大小写。
* `java.lang.Integer#compress` Javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Integer.html#compress(int,int) —— 精确语义与示例。
* *Hacker's Delight*（Henry S. Warren）第 2、7 章 —— 补码、溢出检测、位操作的经典教材。
