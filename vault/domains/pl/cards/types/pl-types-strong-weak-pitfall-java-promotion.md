---
id: pl-types-strong-weak-pitfall-java-promotion
node: types.strong-weak
type: qa
step: 8
---
## Q
Java 里 `'a' + 1` 为什么是 98 而不是 `'b'`？`short s = 1; s = s + 1;` 为什么编译不过而 `s += 1` 却可以？

## A
`char` 在运算前会被提升为 `int`，所以 `'a' + 1` 是 `int` 加 `int`：`'a'` 的编码是 97，结果 98。想要字符 `'b'` 必须写 `(char) ('a' + 1)`。

```java
System.out.println('a' + 1);    // 98
short s = 1;
s += 1;                         // 编译通过
System.out.println(s);          // 2
// s = s + 1;                   // 编译错误
```

实际输出 `98` 和 `2`。取消注释最后一行则编译失败：

```console
error: incompatible types: possible lossy conversion from int to short
```

原因：`s + 1` 里 `s` 先被提升成 `int`，结果是 `int`；把 `int` 赋回 `short` 是缩窄转换，Java 要求显式写 `(short)`。但复合赋值 `s += 1` 在语言规范里等价于 `s = (short) (s + 1)`，它自带一个隐式的强制转换，所以通过编译。这个转换如果溢出了，会静默截断：`short s = 32767; s += 1;` 得到 -32768。

C++ 的对应陷阱出在有符号与无符号混合：编译器把有符号数静默转成无符号再比较。
```cpp
int a = -1; unsigned b = 1;
std::println("{}", a < b);   // false
```
本机输出 `false`：`-1` 被转成 4294967295。clang 要开 `-Wextra` 才会给出 `-Wsign-compare` 警告，默认没有。
教训：复合赋值运算符在 Java 里是一个隐式转换的暗门，同样的表达式写成 `s = s + 1` 和 `s += 1` 并不等价。Go 和 Rust 里没有这个暗门，类型不同的运算一律要求显式转换。
