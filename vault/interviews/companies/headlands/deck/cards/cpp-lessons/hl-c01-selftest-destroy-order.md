---
id: hl-c01-selftest-destroy-order
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 16
---
## Q
```cpp
struct Holder { Tracer first{"f"}; Tracer second{"s"}; ~Holder(){ std::cout << "~Holder body\n"; } };
void f() { Tracer a("a"); Holder h; Tracer c("c"); }
```
函数 `f` 结束时，析构输出顺序是什么？

## A
`dtor c` → `~Holder body` → `dtor s` → `dtor f` → `dtor a`。
- 局部变量按声明顺序的逆序：`c`、`h`、`a`。
- 轮到 `h` 时，先运行 `Holder` 自己的析构函数体，**然后**成员按声明顺序的逆序析构：`second`（"s"）再 `first`（"f"）。
