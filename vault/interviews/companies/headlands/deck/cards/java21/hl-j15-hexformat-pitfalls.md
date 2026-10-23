---
id: hl-j15-hexformat-pitfalls
node: java21.j15-math-string-utils
type: qa
step: 11
---
## Q
`HexFormat.parseHex` 有哪些坑？`0xff` 解析出来是多少？

## A
- 返回的 `byte` 是**有符号**的，`0xff` 读出来是 `-1`（`"0a1bff"` → `{10, 27, -1}`）。
- 要求偶数个字符；
- 用了 `withDelimiter` / `ofDelimiter` 的格式，`parseHex` 也必须用**同一个 `HexFormat` 对象**去解。
- 若要无符号值，用 `Byte.toUnsignedInt(b)` 或 `& 0xff`。
