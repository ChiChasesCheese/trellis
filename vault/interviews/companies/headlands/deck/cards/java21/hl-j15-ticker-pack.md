---
id: hl-j15-ticker-pack
node: java21.j15-math-string-utils
type: qa
step: 16
---
## Q
行情报文里股票代码是 8 字节、右补空格（`"AAPL    "`）。怎么用 `Long.compress` 把它压成 40 位？写出掩码并解释为什么能行。

## A
大写字母 `A..Z` 的 ASCII 是 `0x41..0x5A`，**低 5 位恰是 1..26**；空格 `0x20` 低 5 位是 0。所以每个字节只留低 5 位：

```java
static final long KEEP_LOW5 = 0x1F1F1F1F1F1F1F1FL;
static long pack(String t8) { /* 8 字节拼成 word */ return Long.compress(word, KEEP_LOW5); }
static String unpack(long key) { long spread = Long.expand(key, KEEP_LOW5); /* 还原 + 0x40 */ }
```
8 字节 × 5 位 = 40 位。`A`=00001、`P`=10000、`L`=01100，后面 4 个空格各 00000，完整字段是 `0x0860C00000`；`Long.toHexString` 不显示前导零。`unpack` 后得到 `AAPL`、`MSFT -> MSFT`。
