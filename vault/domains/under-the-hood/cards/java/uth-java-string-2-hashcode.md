---
id: uth-java-string-2-hashcode
node: java.string
type: qa
step: 2
---
## Q
**String 的 hashCode 怎么算、会重复算吗**｜Java · OpenJDK 25

`"Aa"` 和 `"BB"` 的 `hashCode` 为什么相同？`String` 每次调用 `hashCode()` 都重新计算吗？

## A
**结构。** 多项式哈希：`h = 31*h + 字符`，从左到右累加，即 `s[0]*31^(n-1) + … + s[n-1]`。

**细节。**

- 实测 `"Aa".hashCode()` 与 `"BB".hashCode()` 都是 2112：`65*31+97 = 66*31+66`。
- 算出后缓存在 `hash` 字段里，字符串不可变，所以缓存永远有效。
- 结果恰好为 0（包括空串）时不写缓存，而是置 `hashIsZero = true`，避免反复重算。

**为什么。** 不可变换来哈希可缓存，所以 `String` 当 `HashMap` 的 key 很便宜；代价是容易构造冲突，因此 `HashMap` 要有红黑树兜底。

**对应 LeetCode：** LC 49 字母异位词分组 · LC 28 找出字符串中第一个匹配项的下标
