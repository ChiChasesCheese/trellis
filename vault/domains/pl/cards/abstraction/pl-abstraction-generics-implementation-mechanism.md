---
id: pl-abstraction-generics-implementation-mechanism
node: abstraction.generics-implementation
type: qa
step: 5
---
## Q
擦除和单态化在运行时的成本差在哪里？`List<Integer>` 求和比 `int[]` 慢多少，为什么？

## A
擦除版的每个元素访问要做：取引用 → 读堆上的 `Integer` 对象 → 解包出 `int`；元素本身是堆上的小对象，要多一次指针追逐，对缓存不友好。单态化版本（如 Rust 的 `Vec<i32>`）中，元素就在连续内存里，循环可以向量化。

一个测量（Java 25，Apple Silicon，预热后，1000 万个元素顺序求和，一次测量，仅作量级参考）：

```text
List<Integer>  约 15–20 ms
int[]          约 2 ms
```

差距约 7–10 倍。注意这是**对擦除最有利**的情形：元素按顺序分配，在堆上恰好也是连续的。真实程序里对象被打散、年龄不同，指针追逐的成本更高。

三种实现的成本对照：

- **擦除**：代码体积最小，但基本类型要装箱（对象头加引用，约 16–20 字节对 4 字节），并有强转检查。
- **单态化**：运行期无额外成本，体积和编译时间随实例数线性增长。
- **GC shape 加字典**：基本类型不装箱，指针类型的操作多一次字典查找。

所以「Java 泛型慢」更精确的说法是「Java 的泛型容器不能存基本类型」。需要数值性能时，Java 用 `int[]` 或专门的原始类型集合（如 Eclipse Collections 的 `IntList`）。
