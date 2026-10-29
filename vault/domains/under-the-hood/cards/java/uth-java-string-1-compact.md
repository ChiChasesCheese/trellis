---
id: uth-java-string-1-compact
node: java.string
type: qa
step: 1
---
## Q
**Java 字符串一个字符占几个字节**｜Java · OpenJDK 25（Java 9 起）

`"hello"` 和 `"你好世界"` 在 `String` 内部各占多少字节？只混进一个非拉丁字符会怎样？

## A
**结构。** `String` 内部是 `byte[] value` 加一个标志 `coder`：`LATIN1`（每字符 1 字节）或 `UTF16`（每字符 2 字节），整串统一。

**细节。**

- 实测：`"hello world"` 11 个字符占 11 字节，`"héllo"` 5 字节（Latin-1 够用）。
- `"你好世界"` 4 个字符占 8 字节；`"hello€"` 6 个字符占 12 字节：一个 `€` 就让整串变成 UTF-16。
- Java 8 及以前用 `char[]`，每个字符固定 2 字节。

**为什么。** 实际程序里大多数字符串是 Latin-1，字节数组省下约一半内存和缓存；代价是每次取字符要先看 `coder`。

**对应 LeetCode：** LC 3 无重复字符的最长子串 · LC 344 反转字符串
