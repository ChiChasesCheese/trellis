---
id: hl-j15-hexformat
node: java21.j15-math-string-utils
type: qa
step: 10
---
## Q
写出 `HexFormat`（Java 17）的常用调用：转十六进制串、大写、带分隔符和前缀、解析、固定宽度输出。

## A
```java
HexFormat hf = HexFormat.of();
hf.formatHex(bytes)                                  // "0a1bff"
hf.withUpperCase().formatHex(bytes)                  // "0A1BFF"
HexFormat.ofDelimiter(":").withPrefix("0x").formatHex(bytes)  // "0x0a:0x1b:0xff"
hf.parseHex("0a1bff")                                // byte[] {10, 27, -1}
hf.withUpperCase().toHexDigits(48879)                // "0000BEEF"
HexFormat.fromHexDigits("ff")                        // 255
```
`toHexDigits(int)` 总输出**完整宽度**（int 8 位、long 16 位），自动补零，不用手写 `%08x`；`Integer.toHexString` 不补零。
