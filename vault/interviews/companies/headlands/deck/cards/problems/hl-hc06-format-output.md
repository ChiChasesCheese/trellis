---
id: hl-hc06-format-output
node: problems.hc06-cpu-register-bitwise
type: qa
step: 10
---
## Q
寄存器终值的十六进制、十进制、二进制输出在 Java 里怎么写？各自的坑是什么？

## A
```java
public static String hex(int reg) { return "0x" + HexFormat.of().withUpperCase().toHexDigits(reg); }
public static String dec(int reg) { return Integer.toUnsignedString(reg); }
public static String bin(int reg) {
    String raw = Integer.toBinaryString(reg);
    return new StringBuilder(32).repeat('0', 32 - raw.length()).append(raw).toString();
}
```
- `HexFormat.toHexDigits(int)`：固定 8 位、补零、按位模式（`-1 → "FFFFFFFF"`，无负号）；用 `withUpperCase()` 大写；忘补零或用小写都错。
- `Integer.toUnsignedString`：`0xFFFFFFFF` 打成 `4294967295`；用 `Integer.toString` 会打成 `-1`。
- `Integer.toBinaryString` **不补前导零**（5 → `"101"`），要补到 32 位；`toBinaryString(-1)` 本就是 32 个 1。
- `StringBuilder.repeat(char, int)` 是 Java 21，旧写法 `"0".repeat(n)` 多建一个字符串。
- 往返测试验证输出：`parseValue(hex(x)) == unsigned(x)`。

整题 `solve(lines)`：第一个有效行是初值，其余是程序；每个 Query 输出一行十进制，最后一行 `describe(终值)`（`hex dec bin` 空格分隔）。任何 `MalformedProgramException` → 只输出 `Malformed Input`；解析阶段捕获构造器抛的 `IllegalArgumentException` 并转成它。

C++：十进制用 `std::to_string(uint32_t)`；`solve` 里不要 `catch (...)`，会把 `bad_alloc` 也吞成 `Malformed Input`。

测试边界：空程序、只有注释、多余空白、初值 0 / 4294967295 / 4294967296（非法）/ -1（非法）。
