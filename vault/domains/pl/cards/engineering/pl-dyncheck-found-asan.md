---
id: pl-dyncheck-found-asan
node: engineering.dynamic-checkers
type: qa
step: 2
---
## Q
AddressSanitizer（ASan）是怎样发现内存错误的？它的报告长什么样，开销是多少？

## A
**机制**由两部分组成：
1. **替换内存分配器**：每块分配的内存前后各加一段**红区**（redzone，不可访问的填充），被释放的内存先放进隔离队列（quarantine）而不是立即复用，用来抓释放后使用。
2. **影子内存**（shadow memory）：每 8 字节应用内存对应 1 字节影子，记录这 8 字节是否可访问。编译器在每次读写前插入检查：先算出影子地址，影子标记「不可访问」就报错。

**例**（C，作为对照：C 没有任何运行时检查）：

```c
int *a = malloc(4 * sizeof(int));
a[4] = 1;               /* one past the end */
printf("%d\n", a[4]);
```

不加检查直接运行，输出 `1`，退出码 0，bug 完全沉默。用 `clang -fsanitize=address` 编译：

```text
==14396==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000920 at pc ...
WRITE of size 4 at 0x602000000920 thread T0
    #0 0x00010284c85c in main a.c:5
0x602000000920 is located 0 bytes after 16-byte region [0x602000000910,0x602000000920)
allocated by thread T0 here:
    #0 0x000103091274 in malloc+0x78 (libclang_rt.asan_osx_dynamic.dylib)
    #1 0x00010284c804 in main a.c:4
```

报告说明了：访问类型和大小、出错行号、地址相对哪块已分配内存的位置、那块内存是在哪里分配的。

**开销**：官方给出的量级是运行变慢约 2 倍，内存占用增加两三倍。

**在四门语言里的位置**：Go 的 `-asan` 构建选项只对 `cgo` 里的 C 代码有意义；Rust 的稳定版没有 sanitizer，要用 nightly 的 `-Zsanitizer=address`；Java 和 Python 的内存由运行时管理，ASan 只用于它们的本地扩展（JNI、C 扩展）。所以 ASan 在这些语言里的价值，集中在 `unsafe` 和跨语言边界。
