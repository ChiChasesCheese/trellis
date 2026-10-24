---
id: pl-trends-safety-intro-bug-classes
node: trends.safety-push
type: qa
step: 2
---
## Q
内存安全漏洞的两大类（空间错误与时间错误）是什么？在 C 里它们会怎样表现，换到其他语言又变成什么？

## A
**空间错误**（spatial）：访问了不属于这块内存的位置，最常见是缓冲区越界。

```c
int *a = malloc(4 * sizeof(int));
printf("%d\n", a[4]);        // one past the end
```

在没有保护的 C 里，这段代码**正常运行**，打印一个随机数（本机一次运行得到 `-1715467676`），没有崩溃，没有报错。这正是它危险的地方：错误默默发生，数据可能是别的东西的机密。加上 AddressSanitizer 才会报 `heap-buffer-overflow`。

**时间错误**（temporal）：在内存生命周期之外访问，如释放后使用（use-after-free）、重复释放。

```c
char *p = malloc(8); strcpy(p, "hi"); free(p);
printf("%s\n", p);           // p dangles
```

未加保护时输出乱码（本机得到 `\002` 加换行），加 ASan 报 `heap-use-after-free`。攻击者可以精心安排“被释放后又被重新分配的那块内存”的内容，让程序按攻击者的数据行事。

**换成其他语言**：
| 语言 | 越界读取 `a[4]`（长度 4） |
|---|---|
| Python | `IndexError: list index out of range` |
| Go | `panic: runtime error: index out of range [4] with length 4` |
| Rust | `panicked ... index out of bounds` |
| Java | `ArrayIndexOutOfBoundsException` |

四者都在运行时检查并**终止或抛异常**，而不是读到别人的数据。时间错误则靠不同机制消除：GC 语言里只要有引用，对象就不会被回收；Rust 里这样的代码根本无法编译。

**要记住的一点**：内存安全的本质是“错误行为必须是确定的失败，而不是未定义行为”。崩溃是可以接受的后果，悄悄读取别人的数据不是。
