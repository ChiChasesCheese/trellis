---
id: pl-rt-perf-pitfall-pointer-chasing
node: runtime.performance-model
type: qa
step: 9
---
## Q
为什么把 `int[]` 换成 `List<Integer>`，代码几乎没变，遍历却能慢十几倍？

## A
Java 实验（一次测量，1000 万个整数）：
```java
int[] arr = new int[n];                              // contiguous 4-byte values
List<Integer> list = new ArrayList<>(n);             // n references to boxed Integer objects
for (int i = 0; i < n; i++) list.add(arr[i]);
Collections.shuffle(list, rnd);                      // scatter the objects in memory
long s = 0;
for (int i = 0; i < n; i++) s += arr[i];             // loop A
for (int i = 0; i < n; i++) s += list.get(i);        // loop B
```
结果：循环 A（`int[]`）约 **2.1 毫秒**，循环 B（洗牌后的 `ArrayList<Integer>`）约 **31 毫秒**，慢约 15 倍。

原因：
1. 数据布局：`int[]` 是 40 MB 连续的数值；`ArrayList<Integer>` 是 1000 万个引用（约 40 MB）加 1000 万个各 16 字节的 `Integer` 对象（约 160 MB），总共约 5 倍内存。
2. 访问模式：A 顺序读，硬件预取器提前取下一行缓存，每 16 个数才有一次真正的内存延迟；B 每次拿到引用后要跳到一个（洗牌过的）随机地址，几乎每次都缓存未命中，要等主存。
3. 洗牌是为了让对象在内存里的顺序和列表顺序不一致。如果对象是紧挨着按顺序分配的，B 会快很多，所以真实世界里这种代价**取决于对象的分配历史**，难以预测，在长期运行、对象被 GC 搬动、被反复修改之后尤其不可预测。

这是 Java、Python 等“一切皆对象引用”语言的结构性代价：**对象图的性能取决于局部性，而语言不保证局部性。**

对策：
- 热点数据用原始类型数组或专用集合库（fastutil、Eclipse Collections 的原始类型集合）；
- 用“结构体数组变数组的结构体”（SoA）把同类字段放在一起；
- Python 用 `array`、NumPy；
- 等待 Java 的值类（Valhalla）；
- Go、Rust 里的 `[]struct`、`Vec<T>` 天生连续，要避免的是切片里放指针（`[]*T`、`Vec<Box<T>>`）。
