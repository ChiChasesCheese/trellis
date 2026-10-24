---
id: pl-types-static-dynamic-found-compile-errors
node: types.static-dynamic
type: qa
step: 3
---
## Q
在 Go、Java、Rust 里，一个变量的类型是怎样声明的？类型不匹配时编译器会怎样？

## A
三门静态类型语言里，变量（或它的值）在编译前就有确定的类型，编译器逐处核对赋值、传参和运算。类型错误是编译失败，程序不会生成可执行文件。

Go：`var x int = "a"`

```console
./e.go:4:14: cannot use "a" (untyped string constant) as int value in variable declaration
```

Java：`int x = "a";`

```console
E.java:3: error: incompatible types: String cannot be converted to int
```

Rust：`let x: i32 = "a";`

```console
error[E0308]: mismatched types
  expected `i32`, found `&str`
```

三个编译器都给出文件、行号和原因。这就是静态类型的基本交易：你先写下类型（或让编译器推出来），它在构建阶段就挡住一整类错误，上线之后不会再出现「把字符串当整数用」。

同一个错误在 Python 里要等到那行代码真正执行时才出现，而且只有当时变量指向的对象不支持该操作才出错。如果这行在一个很少走到的分支里，可能几个月都不会暴露。
