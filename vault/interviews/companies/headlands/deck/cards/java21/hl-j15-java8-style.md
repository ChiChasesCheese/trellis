---
id: hl-j15-java8-style
node: java21.j15-math-string-utils
type: qa
step: 2
---
## Q
Java 8 风格下，乘法溢出检测、`clamp`、重复字符、十六进制各怎么手写？它们有什么问题？

## A
```java
int px = 2_000_000_000, q = 2;
int notional = px * q;                       // -294967296，没有任何异常
long sum = a + b;
boolean overflow = ((a ^ sum) & (b ^ sum)) < 0;   // 手写溢出检测：符号位技巧，没人看得懂
for (int i = 0; i < 5; i++) sb.append('0');       // 手写循环拼 5 个 0
static int clamp(int v, int lo, int hi) { return Math.max(lo, Math.min(hi, v)); }
String.format("%02x", b)                          // 手写 hex
```
问题：溢出悄悄变成负数；检测靠难读的位技巧；`clamp` 在 `lo > hi` 时悄悄返回 `lo`。Java 8 之后的 `Math.xxxExact`、`Math.clamp`、`StringBuilder.repeat`、`HexFormat` 逐一取代它们。
