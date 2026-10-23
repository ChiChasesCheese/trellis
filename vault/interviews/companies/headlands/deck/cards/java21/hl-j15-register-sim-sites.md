---
id: hl-j15-register-sim-sites
node: java21.j15-math-string-utils
type: qa
step: 22
---
## Q
32 位寄存器模拟里，输出十六进制、补前导零的二进制、限制移位量、模拟 PEXT/PDEP 指令，分别用 Java 21 的哪个 API？

## A
- 固定 8 位大写 hex：`"0x" + HexFormat.of().withUpperCase().toHexDigits(reg)`；
- 二进制补前导零（`Integer.toBinaryString` 不补零）：`new StringBuilder(32).repeat('0', 32 - raw.length()).append(raw).toString()`；
- 移位量限制到 0..32：`args[k] = Math.clamp(c, 0, 32);`
- 模拟 CPU 指令：`Integer.compress(reg, m)` / `Integer.expand(reg, m)`；
- 位计数：`Integer.bitCount(reg)`、`numberOfTrailingZeros(reg)`、`numberOfLeadingZeros(reg)`，对 0 的约定是 32。
