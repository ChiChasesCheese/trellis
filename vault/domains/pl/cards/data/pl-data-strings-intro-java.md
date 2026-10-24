---
id: pl-data-strings-intro-java
node: data.strings-text
type: qa
step: 3
---
## Q
Java 的 `String` 在内存里是什么？`char`、代理对和紧凑字符串（compact strings）怎样共同决定它的行为？

## A
**是什么**：`String` 是不可变对象，内部持有一个数组。逻辑上是 UTF-16 编码单元的序列，`char` 就是一个 16 位的单元。`length()` 返回单元数，`charAt(i)` 取第 i 个单元，二者都 O(1)。

**代理对**：U+FFFF 以上的码点用两个 `char` 表示（一个高代理，一个低代理）。所以一个 emoji 的 `length()` 是 2。要按码点处理，要用 `codePointCount`、`codePoints()` 等方法。

```java
String s = "a😀é";
s.length()                          // 4
s.codePointCount(0, s.length())     // 3
Character.isHighSurrogate(s.charAt(1))  // true
```

上面三行的真实结果是 `4`、`3`、`true`。

**紧凑字符串**（JDK 9 起）：如果字符串的所有字符都在 Latin-1 范围（码点 ≤ 255），内部改用 `byte[]` 每字符 1 字节；否则才用 UTF-16 的 2 字节。这是纯内存优化，对外 API 不变。大部分英文业务字符串因此省一半内存。

**不可变与常量池**：字符串字面量放在常量池里被共享；`s1 == s2` 比较的是引用，内容比较要用 `equals`。不可变使 `String` 可以安全地做 `HashMap` 的键，并缓存哈希值。

**要记住的一点**：Java 的 `char` 不等于「字符」。凡是把 `length()` 当字符数、用 `substring`/`charAt` 按位置截断的代码，在遇到 emoji 时都会出错。
