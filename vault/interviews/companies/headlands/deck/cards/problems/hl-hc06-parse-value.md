---
id: hl-hc06-parse-value
node: problems.hc06-cpu-register-bitwise
type: qa
step: 9
---
## Q
寄存器初值和掩码的数字（十进制 / `0x` / `0b`，范围 0..4294967295）在 Java 里怎么严格解析？为什么不用 `Integer.parseInt` 和 `Long.decode`？

## A
`Integer.parseInt` 是有符号 `int` 范围：`parseInt("4294967295")` 和 `parseInt("FFFFFFFF", 16)` 都抛 `NumberFormatException`，却是 32 位寄存器的合法值。`Long.decode` 把前导 0 当八进制（`"010"` 是 8），还接受 `-` 和 `#`。题面是严格的小语言。

做法：识别前缀 → 逐字符检查 → `Long.parseLong` → 范围检查 → `(int)` 强转（只保留低 32 位，位模式不变）：
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
- `t.length() > 2`：单独的 `"0x"` 不进前缀分支，按十进制解析，`'x'` 被拒；
- 逐字符检查为拒绝 `+1`、`-1`、`1_0`（`Long.parseLong` 本身接受 `+`/`-`）；
- 超过 `long` 抛 `NumberFormatException`，转 `MalformedProgramException`；
- `010` 是十进制 10；`4294967296`、`-1` 非法；`AND 0xFFFFFFFF` 要变成 `And(-1)`（位模式全 1，正是想要的掩码）。
- `toUpperCase(Locale.ROOT)` 避免土耳其语环境的 `İ`；初值用 `long` 传入并检查 `0 ≤ initial ≤ 0xFFFFFFFFL`。

C++：`std::from_chars` 不认 `+` 也不认 `0x`，要自己剥前缀并检查结束指针；`static_cast<uint32_t>(-1LL)` 会变成 `0xFFFFFFFF`，所以参数用 `long long` 先检查范围再转换；`std::toupper/isspace` 传负数 `char` 是 UB，自己写 ASCII 版。
