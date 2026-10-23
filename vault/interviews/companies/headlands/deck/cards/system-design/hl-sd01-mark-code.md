---
id: hl-sd01-mark-code
node: system-design.sd01-unused-code
type: qa
step: 15
---
## Q
用 CSR（compressed sparse row）图和 `BitSet` 写出可达性标记的核心代码，为什么用显式栈？

## A
```java
final class SymbolGraph {
    final int[] offsets;   // 长度 V+1，offsets[v]..offsets[v+1] 是 v 的出边区间
    final int[] targets;   // 长度 E
}
static BitSet mark(SymbolGraph g, int[] rootIds) {
    BitSet live = new BitSet(g.offsets.length - 1);
    int[] stack = new int[1 << 16]; int sp = 0;
    for (int r : rootIds) if (!live.get(r)) { live.set(r); stack = push(stack, sp++, r); }
    while (sp > 0) {
        int v = stack[--sp];
        for (int i = g.offsets[v]; i < g.offsets[v + 1]; i++) {
            int w = g.targets[i];
            if (!live.get(w)) { live.set(w); stack = push(stack, sp++, w); }
        }
    }
    return live;   // 候选 = 非 live 的符号
}
```
显式栈：不递归，调用链再深也不爆栈。连续数组 + `int` 下标对缓存友好，没有 Node / Edge 对象，没有 GC 压力。
