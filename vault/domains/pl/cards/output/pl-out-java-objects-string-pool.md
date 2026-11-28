---
id: pl-out-java-objects-string-pool
node: output.java-objects
type: qa
step: 2
---
## Q
**字符串常量池**｜读代码说输出

```java
public class Main { public static void main(String[] x) {
    String s = "hello", p = "hel";
    final String q = "hel";
    System.out.println(s == "hel" + "lo");
    System.out.println(s == p + "lo");
    System.out.println(s == q + "lo");
    System.out.println(s == (p + "lo").intern());
    System.out.println(s == new String("hello"));
} }
```

输出什么？

## A
**输出。**
```
true
false
true
true
false
```

**为什么。**
- 字面量 `"hello"` 放进字符串常量池（string pool），同内容只有一份；`"hel" + "lo"` 是编译期常量表达式，javac 直接折叠成 `"hello"`，所以和 `s` 是同一个对象，true。
- `p + "lo"` 里 `p` 是普通变量，运行时才拼，生成新对象，false；`q` 是用常量初始化的 `final`，也算常量，折叠后 true。
- `intern()` 返回池里那一份，true；`new String("hello")` 强制新对象，false。

**语言为什么这样设计。**
- JLS 15.29 定义常量表达式，3.10.5 规定它们按 intern 共享，编译器可以合并重复字面量、省内存，`switch` 比较字符串也更便宜。
- 代价是字符串的 `==` 取决于字符串怎么来的。Go 的 string 是值类型，`==` 直接比内容，没有这个问题；Python 的 `is` 同样受 CPython 的驻留（interning）规则影响。

**怎么写才对。**
```java
s.equals(t)            // 比内容
"hello".equals(t)      // 字面量在前，t 为 null 也不抛 NPE
```

**面试里一句话。**
String literals and compile-time constants are interned, but runtime concatenation creates new objects, so compare strings with equals.
