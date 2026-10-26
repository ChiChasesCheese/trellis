# hc06 · 解法与原理

代码不难写，难在每一行背后都有一个语言细节：有符号和无符号读同一串二进制位，结果不同；移位位数超过位宽时，Java 和 C++ 各有各的规则。先说开场 3 分钟怎么做，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "The register is 32 bits unsigned, but Java only has a signed int, so I'll keep it in a long and mask back to 32 bits after every step. Are operands decimal? What should a shift of 32 or more do — I'd say the register becomes zero. And what counts as malformed?"

面试官通常会说：十进制，移位 32 位以上结果是 0，格式错误统一输出 `Malformed Input`。

## Part 1 · 六条指令

**思路**：先写 `num(s)`（把字符串解析成 `0..2³²−1` 的数，不合法就抛异常），再写一个循环：把每行拆成指令名和参数，用 `switch` 更新寄存器，最后输出十进制。所有异常在最外层 `catch` 成 `Malformed Input`。

**原理**

- **32 位无符号怎么存**：同样 32 个 bit，`int` 把最高位当符号位，`0xFFFFFFFF` 读成 `-1`；寄存器要读成 4294967295。Java 里最省事的办法是用 `long` 装，值永远在 `0..2³²−1`，凡是可能溢出 32 位的运算（`NOT`、左移）后面都 `& MASK` 截回去。这样十进制输出、比较、范围检查都不用再区分有符号。
- **不能用 `Integer.parseInt`**：它会拒绝大于 2147483647 的数，而 `AND 4294967295` 是合法的。用 `Long.parseLong`，再检查范围。解析前先用正则 `\d{1,10}` 过滤，拒绝 `-1`、`+5`、空串；最长 10 位，也避免了超长字符串。
- **逻辑右移**：`>>>` 高位补 0。`>>` 会补符号位，在 `int` 里对最高位为 1 的值（比如 `NOT` 之后）会带进一串 1。因为寄存器放在 `long` 里、高 32 位恒为 0，这里 `>>>` 和 `>>` 碰巧相同，但写成 `>>>` 才表达你的意图。
- **移位 32 位及以上**：Java 里 `int` 的移位位数只取低 5 位（`k & 31`），所以 `x << 32 == x`；C++ 里移位位数大于等于位宽是未定义行为（undefined behavior，UB）。题目要的硬件语义是所有位都被挤出去、结果为 0，所以必须写 `k >= 32 ? 0 : ...`。
- **参数个数**：`NOT` 必须没有参数，其余必须恰好一个参数。

**Java**

```java
private static final long MASK = 0xFFFFFFFFL;

private static long num(String s) {
    if (!s.matches("\\d{1,10}")) throw new IllegalArgumentException("not a number: " + s);
    long v = Long.parseLong(s);
    if (v > MASK) throw new IllegalArgumentException("out of range: " + s);
    return v;
}

public static List<String> solve(List<String> lines) {
    try {
        long r = num(lines.get(0));
        for (String line : lines.subList(1, lines.size())) {
            String[] p = line.trim().split("\\s+");
            if (p.length != (p[0].equals("NOT") ? 1 : 2)) throw new IllegalArgumentException("bad line: " + line);
            long a = p.length == 2 ? num(p[1]) : 0;
            switch (p[0]) {
                case "AND" -> r &= a;
                case "OR" -> r |= a;
                case "XOR" -> r ^= a;
                case "NOT" -> r = ~r & MASK;
                case "SHL" -> r = a >= 32 ? 0 : r << a & MASK;
                case "SHR" -> r = a >= 32 ? 0 : r >>> a;
                default -> throw new IllegalArgumentException("unknown op: " + p[0]);
            }
        }
        return List.of(Long.toString(r));
    } catch (RuntimeException e) {
        return List.of("Malformed Input");
    }
}
```

**C++**

```cpp
inline std::uint32_t num(const std::string& s) {
    if (s.empty() || s.size() > 10 || s.find_first_not_of("0123456789") != std::string::npos) throw std::invalid_argument("not a number");
    unsigned long long v = std::stoull(s);
    if (v > 0xFFFFFFFFULL) throw std::invalid_argument("out of range");
    return static_cast<std::uint32_t>(v);
}

inline std::vector<std::string> solve(const std::vector<std::string>& lines) {
    try {
        std::uint32_t r = num(lines.at(0));
        for (std::size_t i = 1; i < lines.size(); ++i) {
            std::istringstream in(lines[i]);
            std::vector<std::string> p{std::istream_iterator<std::string>(in), {}};
            if (p.empty() || p.size() != (p[0] == "NOT" ? 1u : 2u)) throw std::invalid_argument("bad line");
            std::uint32_t a = p.size() == 2 ? num(p[1]) : 0;
            if (p[0] == "AND") r &= a;
            else if (p[0] == "OR") r |= a;
            else if (p[0] == "XOR") r ^= a;
            else if (p[0] == "NOT") r = ~r;
            else if (p[0] == "SHL") r = a >= 32 ? 0 : r << a;
            else if (p[0] == "SHR") r = a >= 32 ? 0 : r >> a;
            else throw std::invalid_argument("unknown op");
        }
        return {std::to_string(r)};
    } catch (const std::exception&) {
        return {"Malformed Input"};
    }
}
```

C++ 的 `std::uint32_t` 本来就是无符号 32 位，不需要掩码，`~r` 的结果自动留在 32 位里。

复杂度：时间 O(指令数)，空间 O(1)。

## Part 2 · 循环移位和输出格式

**思路**：先加 `ROL` / `ROR`：位数先对 32 取模得 `k`，左移 `k` 位的同时把最高的 `k` 位用右移 `32 - k` 位挪到最低位，两部分按位或。再处理格式：解析前先看最后一行是不是 `DEC` / `HEX` / `BIN`，是就记下来并从指令里去掉，否则默认 `DEC`。

**原理**

- **`k = 0` 的陷阱**：右移 `32 - k` 位在 `k = 0` 时是右移 32 位。C++ 里这是 UB（寄存器是 `uint32_t`），必须单独写 `k == 0 ? r : ...`。Java 里因为寄存器放在 `long` 里，右移 32 位是正常的右移，值恰好是 0，结果碰巧对；如果寄存器用 `int`，`x >>> 32 == x`，也碰巧对，但原因不同，别靠它。更稳的写法是 Java 用 `Integer.rotateLeft(x, k)`，C++20 用 `std::rotl(x, k)`，它们对任何 `k` 都有定义，编译器还会换成一条旋转指令。
- **`ROR` 就是 `ROL` 反过来**：右移 `k` 位的同时，最低的 `k` 位挪到最高位。
- **格式只能在最后一行**：先看最后一行（行数大于 1 才算，免得把初值当格式），是格式就拿走。如果 `HEX` 出现在中间，它到了指令循环里就是未知指令，自然 `Malformed Input`。
- **输出**：`HEX` 用 `%08X` 补零到 8 位；`BIN` 在 Java 里用 `Long.toBinaryString` 再左补 0 到 32 位，C++ 里 `std::bitset<32>::to_string()` 直接给出 32 位。

**Java**

```java
public static List<String> solve(List<String> lines) {
    try {
        long r = num(lines.get(0));
        int end = lines.size();
        String fmt = lines.get(end - 1);
        if (end > 1 && (fmt.equals("DEC") || fmt.equals("HEX") || fmt.equals("BIN"))) end--; else fmt = "DEC";
        for (String line : lines.subList(1, end)) {
            String[] p = line.trim().split("\\s+");
            if (p.length != (p[0].equals("NOT") ? 1 : 2)) throw new IllegalArgumentException("bad line: " + line);
            long a = p.length == 2 ? num(p[1]) : 0;
            int k = (int) (a % 32);
            switch (p[0]) {
                case "AND" -> r &= a;
                case "OR" -> r |= a;
                case "XOR" -> r ^= a;
                case "NOT" -> r = ~r & MASK;
                case "SHL" -> r = a >= 32 ? 0 : r << a & MASK;
                case "SHR" -> r = a >= 32 ? 0 : r >>> a;
                case "ROL" -> r = (r << k | r >>> (32 - k)) & MASK;
                case "ROR" -> r = (r >>> k | r << (32 - k)) & MASK;
                default -> throw new IllegalArgumentException("unknown op: " + p[0]);
            }
        }
        return List.of(switch (fmt) {
            case "HEX" -> String.format("0x%08X", r);
            case "BIN" -> String.format("%32s", Long.toBinaryString(r)).replace(' ', '0');
            default -> Long.toString(r);
        });
    } catch (RuntimeException e) {
        return List.of("Malformed Input");
    }
}
```

**C++**

```cpp
inline std::vector<std::string> solve(const std::vector<std::string>& lines) {
    try {
        std::uint32_t r = num(lines.at(0));
        std::size_t end = lines.size();
        std::string fmt = lines.back();
        if (end > 1 && (fmt == "DEC" || fmt == "HEX" || fmt == "BIN")) --end; else fmt = "DEC";
        for (std::size_t i = 1; i < end; ++i) {
            std::istringstream in(lines[i]);
            std::vector<std::string> p{std::istream_iterator<std::string>(in), {}};
            if (p.empty() || p.size() != (p[0] == "NOT" ? 1u : 2u)) throw std::invalid_argument("bad line");
            std::uint32_t a = p.size() == 2 ? num(p[1]) : 0, k = a % 32;
            if (p[0] == "AND") r &= a;
            else if (p[0] == "OR") r |= a;
            else if (p[0] == "XOR") r ^= a;
            else if (p[0] == "NOT") r = ~r;
            else if (p[0] == "SHL") r = a >= 32 ? 0 : r << a;
            else if (p[0] == "SHR") r = a >= 32 ? 0 : r >> a;
            else if (p[0] == "ROL") r = k == 0 ? r : r << k | r >> (32 - k);
            else if (p[0] == "ROR") r = k == 0 ? r : r >> k | r << (32 - k);
            else throw std::invalid_argument("unknown op");
        }
        if (fmt == "BIN") return {std::bitset<32>(r).to_string()};
        if (fmt == "HEX") { char buf[16]; std::snprintf(buf, sizeof buf, "0x%08X", r); return {buf}; }
        return {std::to_string(r)};
    } catch (const std::exception&) {
        return {"Malformed Input"};
    }
}
```

复杂度：同 Part 1。

## Part 3 · 口头追问和回答

**1. Java 没有无符号 `int`，你怎么表示这个寄存器？**

两种办法。一是用 `long` 装，值始终在 `0..2³²−1`，每步把可能溢出 32 位的结果 `& 0xFFFFFFFFL`；输出和比较都不用特殊处理，代价是每次要记得截断。二是用 `int` 装位模式：位运算（`& | ^ ~ <<`）只看位，有没有符号都一样，只有三类操作要换成无符号版本：右移用 `>>>`，转十进制用 `Integer.toUnsignedString`（或 `Integer.toUnsignedLong`），比较用 `Integer.compareUnsigned`；解析输入用 `Integer.parseUnsignedInt`。不能写 `(long) reg`：它会符号扩展，`-1` 变成 `-1L`，不是 4294967295。

**2. 为什么 `SHL 32` 要单独处理？**

Java 的 `int` 移位只取位数的低 5 位，`x << 32` 等于 `x << 0`，也就是 `x` 本身，不是 0。C++ 里移位位数大于等于位宽是未定义行为，编译器可以做任何事，开 UBSan 会直接报错。题目要的是硬件意义上的「所有位都被挤出去」，结果为 0，所以要自己判断 `k >= 32`。

**3. `>>` 和 `>>>` 有什么区别？这里该用哪个？**

`>>` 是算术右移，高位补原来的符号位；`>>>` 是逻辑右移，高位补 0。无符号寄存器的右移要补 0，所以应该用 `>>>`。用 `>>` 的后果：`int` 里最高位为 1 的值（比如 `NOT` 之后）会带进一串 1。C++ 里 `uint32_t` 的 `>>` 本来就是逻辑右移。

**4. 循环移位怎么写才不会出错？`ROL 0` 为什么是陷阱？**

标准写法是 `(x << k) | (x >> (32 - k))`，`k` 先对 32 取模。`k = 0` 时第二项是右移 32 位：C++ 里是 UB，所以要单独判断 `k == 0`。更好的做法是直接用库函数：Java 的 `Integer.rotateLeft`，C++20 的 `std::rotl`，它们对任何位数都有定义，编译后是一条旋转指令。

**5. 如果寄存器是 64 位，哪些地方要改？**

位运算部分把 `int` / `long` 换成 `long` / `uint64_t`，移位的界限从 32 改成 64，`MASK` 不再需要（`long` 本来就是 64 位，已经装满）。Java 里要用 `Long.parseUnsignedLong` 解析、`Long.toUnsignedString` 输出，因为 `long` 也是有符号的，`2⁶⁴−1` 在 `long` 里是 `-1`；范围检查也不能再用「放进更大的类型再比较」的办法，要靠 `parseUnsignedLong` 自己抛异常。

**6. 为什么不能用 `Integer.parseInt` 解析操作数？**

它只接受 `-2³¹..2³¹−1`，`4294967295` 会抛 `NumberFormatException`，但这是一个合法操作数。另外它还接受 `+5` 和 `-5`，而题目只允许不带符号的十进制，所以要先用正则或逐字符检查，再用 `Long.parseLong` 解析并检查范围。

## 常见错误

1. 把寄存器放在 `int` 里，输出时直接 `Integer.toString`：最高位为 1 的值打印成负数。
2. 右移写成 `>>`：`int` 里最高位为 1 时高位被补上 1。
3. 移位不判断 `k >= 32`：Java 里 `x << 32 == x`，C++ 里是 UB。
4. 循环移位在 `k = 0` 时右移 32 位：C++ 里是 UB。
5. 用 `Integer.parseInt` 解析操作数：大于 2147483647 的合法值被当成错误。
6. `HEX` 输出忘了补零，或者用 `%x` 输出小写：`0xFF` 而不是 `0x000000FF`。
