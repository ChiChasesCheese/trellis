---
id: hl-javaq-d-q15-substring-hot
node: java-questions.d-memory
type: qa
step: 20
---
## Q
`substring` 现在是拷贝还是共享？字符串去重（deduplication）是什么？交易系统的 symbol 在热路径上怎么存？Java 有没有 `string_view` 对应物？

## A
- **`substring`**：7u6 起**拷贝**，不再共享底层数组，小子串不会钉住大字符串，但是 O(k)。
- **去重**：`intern()` 是手动；`-XX:+UseStringDeduplication`（G1，默认关）由 GC 在后台去重底层数组。
- **tick 的 symbol**：别拿 `String` 做热路径 key；预先映射到 `int` id，或存 `byte[]` / `long`（8 字符 packed）。
- **`string_view`**：Java 没有零拷贝视图，`CharSequence` / `ByteBuffer.slice()` 是近似物。
