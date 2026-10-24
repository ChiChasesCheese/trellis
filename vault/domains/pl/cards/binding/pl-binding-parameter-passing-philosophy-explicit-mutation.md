---
id: pl-binding-parameter-passing-philosophy-explicit-mutation
node: binding.parameter-passing
type: qa
step: 8
---
## Q
为什么 Rust 要求调用点写 `&mut x`，而 Java、Python 调用 `list.add(x)` 时看不出会修改？「调用点可见的可变性」背后是什么设计取舍？

## A
同一个操作「函数改了我的数据」，在不同语言里**谁能事先知道**差别很大：

- **Python / Java**：`process(items)` 看不出 `items` 会不会被改。要靠函数名（`sort` 对 `sorted`）、文档、约定。Python 标准库刻意用两套名字区分：`list.sort()` 原地排序返回 `None`，`sorted(xs)` 返回新列表。
- **Go**：传指针 `process(&cfg)` 表示可能被改；传值则不会。切片和 map 是例外，`sort.Ints(xs)` 看起来像传值，实际改了 `xs`。
- **Rust**：`process(&mut items)`，调用点必须写 `&mut`，连「这个局部变量允许被借走修改」也要先声明 `let mut items`。

三种做法对应不同的价值观：

1. 动态语言和 Java 假设**程序员记得住**，语法越轻越好，别名带来的意外靠测试和评审发现。
2. Go 假设**读代码的人没有时间查文档**，所以把「会不会改」的信息尽量放在调用点（指针 `&`），但为了让切片好用，容忍了一个例外。
3. Rust 假设**错误应该在编译时被证明不存在**，因此可变性是类型系统的一部分，而不是约定。

调用点可见的代价是啰嗦，收益是评审时一眼就能锁定「这里会改状态」。在大型代码库里，评审者阅读代码的时间远多于作者写的时间，把信息放在读者眼前是划算的。

对 Java、Python 工程师的启示：当你无法让语言替你标注，就用命名与不可变数据代替。比如函数名里体现动作（`sortInPlace`），或者默认返回新对象、不修改入参（`List.copyOf`、`tuple`、`frozen dataclass`）。

结论：参数传递的哲学差异，本质是「可变性的信息放在哪里」：类型里（Rust）、调用点（Go 的指针）、还是约定里（Java、Python）。
