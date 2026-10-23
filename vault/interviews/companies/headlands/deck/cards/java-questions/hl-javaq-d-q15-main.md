---
id: hl-javaq-d-q15-main
node: java-questions.d-memory
type: qa
step: 17
---
## Q
Java 的 `String` 是怎么实现的？讲不可变性、驻留（interning）、循环里用 `+`、hash 缓存、`substring`。
How are Java `String`s implemented? Immutability, interning, `+` in a loop, hash caching, `substring`.

## A
一句话：`String` **不可变**，内部是 `byte[]` + 编码标志（紧凑字符串：Latin-1 一字节、否则 UTF-16）；`hashCode` 缓存在对象里；字面量进常量池，可 `intern`；`substring` 拷贝；循环里 `+=` 是 O(n²)。

- 内存：对象头 + `value`（指向 `byte[]`）+ `coder`（0 = LATIN1，1 = UTF16）+ 缓存的 `hash`。
- 不可变带来：可安全共享、线程安全、可缓存 hash、可作 map key、字面量池化；代价是每次修改产生新对象。
- 所以 `String` 是好的 `HashMap` 键：不可变且缓存 hash。
