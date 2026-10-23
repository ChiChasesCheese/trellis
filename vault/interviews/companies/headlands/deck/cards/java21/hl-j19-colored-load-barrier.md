---
id: hl-j19-colored-load-barrier
node: java21.j19-runtime-zgc-jit
type: qa
step: 14
---
## Q
ZGC 怎么做到「搬家时应用还在读写」？着色指针（colored pointers）和加载屏障（load barrier）各是什么？

## A
1. **着色指针**：对象引用里挪出几位当「状态标记」（引用是否已检查过、指向的对象是否已被搬走）。这也是 ZGC 不用压缩指针（compressed oops）的原因之一，同样的对象图占内存略多。
2. **加载屏障**：**应用线程每从堆里读一个引用**，JIT 都在后面插一小段检查；若「颜色」表示对象已搬家，屏障就帮着找到新地址、修好这个引用（self-healing），应用线程继续往下走。
