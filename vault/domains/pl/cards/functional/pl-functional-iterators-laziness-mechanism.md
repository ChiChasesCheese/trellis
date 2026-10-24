---
id: pl-functional-iterators-laziness-mechanism
node: functional.iterators-laziness
type: qa
step: 6
---
## Q
一条 `filter -> map -> sum` 流水线在 Rust、C++、Java、Python、Go 里分别怎么执行？为什么说 Rust 的是「零成本」？

## A
- **Rust**：每个适配器是一个泛型结构体（`Map<Filter<Iter<i32>, F1>, F2>`），`next()` 层层调用内层的 `next()`。因为是泛型加闭包，全部被单态化并内联，整条链编译成一个循环。实测（aarch64，`-O`）把 `v.iter().filter(|x| x % 2 == 0).map(|x| x * 3).sum()` 与手写的 `for` 加 `if` 循环分别编译，两个函数都是 87 条指令，都被自动向量化。这是「你用的抽象，手写也不会更好」的实例。
- **Java**：Stream 是一串 `Sink` 对象，每个阶段把元素推给下一个阶段。逐个元素穿过流水线，没有中间集合。JIT 能把这条链内联，但依赖预热和类型分布；`Stream<Integer>` 每个元素要装箱，数值场景用 `IntStream`。
- **C++**：ranges 视图也是泛型对象（`filter_view<…>` 套 `transform_view<…>`），模板展开后同样可内联成一个循环。但实测它不一定等于手写循环（aarch64，`-O2`，1 亿个 `int`，一次测量）：

```cpp
for (int x : v | std::views::filter([](int x) { return x % 2 == 0; })
               | std::views::transform([](int x) { return x * 3; })) s += x;
// versus: for (int x : v) if (x % 2 == 0) s += x * 3;
```
视图版约 24 毫秒、手写循环约 8 毫秒（慢约 3 倍），结果相同。汇编里手写循环被自动向量化（107 条指令），视图版没有（29 条标量指令）。「零开销」是目标不是保证，要用基准确认。
- **Python**：生成器每次 `next()` 恢复一个挂起的函数帧，执行到下一个 `yield`。没有内联，每个元素每一阶段都是一次 Python 级别的调用，所以链很长时明显慢于 C 实现的内置函数（`sum`、`sorted`）。
- **Go**：range-over-func 把循环体编译成一个闭包传给序列函数。序列函数很简单时，编译器可以内联并消除闭包；复杂时就是一次间接调用。

共同的结构是**拉通**：一个元素处理完整条流水线，再取下一个，所以内存是 O(1)（不需要中间集合）。

差异在于编译器看到多少：Rust 在编译期看到所有类型并展开；Java 靠运行期统计；Python 和 Go 看到的较少。惰性本身有成本——每个元素在每一阶段上的调用——Rust 通过内联抹掉它，其他语言则不同程度地承担。
