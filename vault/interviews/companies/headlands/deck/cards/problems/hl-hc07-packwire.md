---
id: hl-hc07-packwire
node: problems.hc07-ticker-hash-map
type: qa
step: 10
---
## Q
行情报文里的 ticker 字段（8 字节，大写字母 + 右侧补空格）怎么用 `Long.compress` 和 `VarHandle` 一步打包成 key？

## A
报文字段如 `"AAPL    "`。关键观察：字母 `A..Z` 的 ASCII 是 `0x41..0x5A`，**低 5 位恰好是 1..26**；空格 `0x20` 的**低 5 位恰好是 0**。所以把 8 个字节每个的低 5 位拼起来就是编码：

```java
private static final VarHandle BE_LONG =
    MethodHandles.byteArrayViewVarHandle(long[].class, ByteOrder.BIG_ENDIAN);
long word = (long) BE_LONG.get(buf, off);       // 一次读 8 字节，越界抛 IndexOutOfBoundsException
// 校验：字母……尾部空格；首字节不能是空格
return Long.compress(word, 0x1F1F1F1F1F1F1F1FL);   // 每个字节的低 5 位拼成连续 40 比特
```
- 大端读出，第一个字节在最高位，对应第一个字符，与编码方向一致；
- `Long.compress(x, mask)`（Java 19）把 `x` 中 `mask` 为 1 的比特按顺序拼到低位，x86 上 JIT 成 `PEXT`；旧写法 8 次「取字节、掩码、移位、或」；
- `byteArrayViewVarHandle` 把 `byte[]` 看成 `long[]` 视图，自带边界检查，不分配 `ByteBuffer`；
- 非法（全空格、前导空格、中间空格、小写、非字母、`\0`）→ `IllegalArgumentException`；`off+8 > buf.length` 或 `off < 0` → `IndexOutOfBoundsException`；
- 校验用一个 8 次小循环：字母，然后尾部空格。

C++：`memcpy` 进 `uint64_t` + `bswap`；字节序用 `std::endian`；`off + 8 > size` 在 `off` 接近 `SIZE_MAX` 时回绕，应先保证 `size >= 8` 再写 `off > size - 8`；`char` 有符号，只检查上界会放过 `0xC3`；`isalpha/toupper` 传负数是 UB。
