---
id: hl-javaq-d-q15-say60
node: java-questions.d-memory
type: qa
step: 32
---
## Q
用英文 60 秒回答：How are Java `String`s implemented? Immutability, interning, `+` in a loop, hash caching, `substring`.

## A
结构：不可变加 byte 数组加 coder → hash 缓存实测 → 常量池与 intern 使 `==` 成陷阱 → `+` 用 indy 但循环里仍是平方 → substring 拷贝 → 热路径别用 String 做 key。

> "A `String` is immutable and backed by a byte array plus a coder flag - since Java 9 Latin-1 text takes one byte per character. The hash code is cached in the object, so the second `hashCode()` on a 50-million-character string took zero microseconds in my test versus 32 milliseconds the first time. Literals live in a constant pool and `intern()` returns the pooled instance, which is why `==` on strings is a trap. `+` compiles to `invokedynamic`, but concatenating in a loop is still quadratic - 80,000 appends took about 100 ms versus under a millisecond with `StringBuilder`. `substring` copies since Java 7u6. On a hot path I wouldn't use strings as keys - I'd map symbols to ints or packed longs."
