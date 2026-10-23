---
id: hl-javaq-c-q10-say60
node: java-questions.c-languages
type: qa
step: 19
---
## Q
用英文 60 秒回答：How do Java generics differ from C++ templates? What is type erasure and what does it cost?

## A
结构：擦除 vs 按类型实例化 → 装箱 = 引用数组 → 实测约 5 倍内存 → 热路径用原始类型数组 → 根本解法 Valhalla 尚未在 21 中。

> "Java generics are erased: the compiler checks types and then everything becomes `Object` at run time, so a `List<Integer>` is an array of references to boxed Integers. C++ templates instantiate separate code per type, so a `vector<int>` is a contiguous array of ints. The cost in Java is boxing: in my measurement a million-element `ArrayList<Integer>` took about five times the memory of an `int[]`, and iteration chases pointers. So on hot paths I use primitive arrays or primitive-specialised collections; the language-level fix, value classes, is the Valhalla work and isn't in 21."
