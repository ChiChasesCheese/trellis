---
id: pl-rt-linking-found-symbols
node: runtime.linking-abi
type: qa
step: 2
---
## Q
目标文件（object file）里的符号（symbol）和重定位（relocation）是什么？“undefined symbol”这类链接错误是怎么产生的？

## A
编译器把一个源文件编译成**目标文件**：里面是机器码，以及一张**符号表**。符号就是带名字的东西（函数、全局变量），分两类：**已定义**（这个文件里有）和**未定义**（引用了别的文件的）。因为调用方不知道目标地址，调用指令里先留空，旁边记一条**重定位项**：“这个位置要填符号 `helper` 的地址”。

用 C 的两个文件看最清楚：
```
a.c: int main(void) { return helper(41) - 42; }
b.c: int helper(int x) { return x + 1; }
$ nm a.o b.o
a.o:  U _helper        <- undefined, to be found elsewhere
      T _main          <- defined here (T = text/code)
b.o:  T _helper
```
`otool -rv a.o` 显示一条重定位：`BR26 ... _helper`（一条分支指令的目标待填）。

**链接器**做的事：收集所有目标文件和库，把每个未定义符号匹配到一个定义，给所有代码和数据分配最终地址，再回到每个重定位位置把地址填进去。只链接 `a.o` 不给 `b.o` 时报错：
```
Undefined symbols for architecture arm64:
  "_helper", referenced from: _main in a.o
```
链接 `a.o b.o` 后能运行，退出码 0（41 + 1 = 42）。

对各语言的含义：
- **Go**：编译产物用 `go tool nm` 能看到 `main.main` 等符号，所有 Go 包用同一个链接器（Go 自带，不用系统的 `ld`）链接。
- **Rust**：符号名被**重整**（mangling），把类型和泛型参数编进名字，如 `_RINvMNtNtCs...`；这既避免重名，也是 Rust 没有稳定 ABI 的一个表现。
- **Java/Python**：没有这一步。方法引用在类文件里是“类名 + 方法名 + 描述符”的字符串，由 JVM 在运行时解析；Python 的名字在运行时的字典里查找。

本质：**链接就是一次“按名字查找并填地址”**，静态的发生在构建时，Java/Python 的发生在运行时。
