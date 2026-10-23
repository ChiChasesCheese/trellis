---
id: hl-j15-formatted-repeat
node: java21.j15-math-string-utils
type: qa
step: 9
---
## Q
`String.formatted` 和 `StringBuilder.repeat` 怎么用？各自的版本和参数含义是什么？

## A
```java
"TRADE taker=%d maker=%d px=%d qty=%d".formatted(3, 1, 18950, 100)
new StringBuilder().repeat('0', 32 - bin.length()).append(bin)  // 补前导零
new StringBuilder().repeat("ab", 3)                              // "ababab"
```
- `formatted`（Java 15）是**实例方法**，等价于 `String.format(同样的串, 参数...)`，能直接接在文本块后面。
- `StringBuilder.repeat`（Java 21）：`repeat(int codePoint, int count)` 与 `repeat(CharSequence, int count)`。第一个形参是 `int` **码点**（code point），写 `'0'` 时 char 自动提升。
- `String.repeat(int)`（Java 11）早有，`StringBuilder.repeat` 用于不想先建临时 `String` 时。
