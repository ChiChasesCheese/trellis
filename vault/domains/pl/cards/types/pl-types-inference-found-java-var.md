---
id: pl-types-inference-found-java-var
node: types.inference
type: qa
step: 2
---
## Q
Java 的 `var` 和钻石运算符 `<>` 分别让编译器推导什么？推导的依据是什么？

## A
`var`（Java 10 起）用在局部变量声明上，编译器根据初始化表达式的类型填入变量类型。它只是省掉了你写的那一遍，变量仍然是静态类型的，之后不能指向别的类型。限制：只能用于局部变量，不能用于字段、方法参数或返回值，也不能配 `null` 或没有初始化器的声明。

钻石运算符 `<>`（Java 7 起）用在 `new` 表达式上，泛型参数由赋值左边的声明类型推出来，不用重复写。

```java
var n = 42;                              // int
var names = new ArrayList<String>();     // ArrayList<String>
List<String> more = new ArrayList<>();   // <> 由左边的 List<String> 补全
names.add("x");
System.out.println(names + " " + more);  // [x] []
```

实际输出 `[x] []`。三行的类型都在编译期确定，只是书写省略了。

两者的信息来源方向不同：`var` 从右往左（用右边的值定左边变量的类型），`<>` 从左往右（用左边的声明定右边的泛型参数）。当两个省略同时出现，如 `var list = new ArrayList<>()`，信息两头都缺，编译器只能退化到 `Object`。
