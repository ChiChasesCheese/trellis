---
id: hl-j18-inference-blindspot
node: java21.j18-comparators-interfaces
type: qa
step: 16
---
## Q
为什么 `Comparator.comparing(p -> p.name()).reversed()` 编译失败？有哪三种修法？

## A
报错 `cannot find symbol: method name() location: variable p of type Object`：lambda 参数 `p` 被推导成 `Object`。因为 `.reversed()` 接在后面，编译器无法用目标类型 `Comparator<P>` 反推 `comparing` 的 `T`。

修法：
1. 方法引用：`Comparator.comparing(P::name).reversed()`；
2. 显式类型参数：`Comparator.<P, String>comparing(p -> p.name())`；
3. 显式 lambda 参数类型：`(P p) -> p.name()`。

实际代码里 k 路合并的堆比较器就写成 `Comparator.<Head<T>, T>comparing(h -> h.value).thenComparingInt(h -> h.stream)`，值相同按流编号 tie-break，保证稳定确定。
