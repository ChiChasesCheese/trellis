---
id: pl-dyncheck-pitfall-redzone-jump
node: engineering.dynamic-checkers
type: qa
step: 8
---
## Q
一次 ASan 运行没有任何报告，是否说明程序没有内存错误？举一个 ASan 漏报的例子。

## A
不能。动态检查器有两类盲区：**没执行到的路径**根本不会被检查；**检查机制的边界**也会漏报。

ASan 靠红区抓越界：红区只有有限的宽度（本例中每块分配前后约 16 字节）。如果越界访问「跳过」红区，正好落在另一块合法分配的内存里，影子内存显示该地址可访问，ASan 就不会报错。

**例**（C，`clang -fsanitize=address` 构建）：

```c
char *a = malloc(16);
char *b = malloc(16);
b[0] = 'B';
long gap = b - a;             /* distance between the two blocks */
a[gap] = 'X';                 /* "overflow" that lands inside b */
printf("b[0]=%c gap=%ld\n", b[0], gap);
```

输出：

```text
b[0]=X gap=32
```

`a[32]` 远远超出了 `a` 的 16 字节，却落进了 `b` 的范围：`b[0]` 被悄悄改成了 `X`，没有任何报告。

**这意味着**：
- 干净的运行只能说明「这次执行的这些访问没触发检测」，不是证明；
- 越界的跨度越大、随机性越强（比如被攻击者控制的下标），越容易越过红区；
- 释放后使用同理：对象被隔离队列放出后，内存可能已经被别的分配占用，旧指针访问到的又是合法地址。

**对策**：配合其他手段叠加覆盖。用 fuzz 提高被执行的路径数量；用 Miri 之类基于指针来源（provenance）的检查器抓「地址合法但权限不对」的访问；对关键代码做边界检查或使用安全的抽象（切片、迭代器），把检查前移到编译期；保持 ASan 的红区宽度设置在较大值（`ASAN_OPTIONS=redzone=...`）能缩小漏洞，但不能消除。
