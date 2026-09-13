---
id: leetcode-c-java-enumset-bit-vector-application
node: topics.uncategorised
type: qa
anki: 1787361364249
tags: [algorithm::bitset, algorithm::ordinal-mapping, algorithm::set-algebra, application, case, case::java-enumset-bit-vector, category::runtimes-os, chapter::05, chapter::16, leetcode, system::openjdk-enumset]
---
## Q
为什么 `EnumSet` 的 union/intersection 能比普通 `HashSet` 更直接？最大的语义坑是什么？

## A
enum ordinal 映射到 bit position，union/intersection 直接是 OR/AND。最大的坑是 ordinal 随声明顺序变化，不应把内部 bit mask 当稳定持久化格式。

**Evidence**

Java API 说明 EnumSet 内部表示为 bit vector；OpenJDK RegularEnumSet 使用 single long。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FJava%20EnumSet%EF%BC%9A%E4%B8%80%E4%B8%AA%20long%20%E4%BF%9D%E5%AD%98%E6%9E%9A%E4%B8%BE%E9%9B%86%E5%90%88)
