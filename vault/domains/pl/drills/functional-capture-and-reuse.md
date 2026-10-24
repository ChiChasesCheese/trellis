---
nodes: [functional.closures, functional.iterators-laziness, functional.generators]
tags: [drill]
---
# 练习：循环里创建的闭包捕获了什么，迭代器能不能用第二遍

一位同事把一段 Python 数据流水线移植到 Go、Java 和 Rust，结果两处出问题：循环里注册的回调全部拿到同一个下标；流水线的第二次遍历悄悄变成空结果，没有任何报错。你要预测五段代码的输出，并解释为什么这两类问题在四门语言里的暴露方式完全不同。

```python
fs = [lambda: i for i in range(3)]
print([f() for f in fs])
gen = (x * x for x in range(3))
print(list(gen), list(gen))
```

```go
var fs []func() int
for i := 0; i < 3; i++ { fs = append(fs, func() int { return i }) }
// 依次运行 fs[0]()、fs[1]()、fs[2]()：分别在 go.mod 写 go 1.21 和 go 1.22 时
```

```java
for (int i = 0; i < 3; i++) { fs.add(() -> i); }          // 能编译吗？
Stream<Integer> s = Stream.of(1, 2, 3).map(x -> x * x);
s.toList(); s.toList();                                    // 第二次调用会怎样？
```

```rust
let fs: Vec<Box<dyn Fn() -> i32>> = (0..3).map(|i| Box::new(move || i) as Box<dyn Fn() -> i32>).collect();
let it = (1..4).map(|x| x * x);
let a: Vec<i32> = it.collect();
let b: Vec<i32> = it.collect();                            // 能编译吗？
```

**要你给出的**
- 每段代码的结果（输出、异常或编译错误），以及 Python 里让回调拿到各自下标的两种写法。
- Go 迭代器函数（`iter.Seq`）被 `range` 遍历两次时会怎样。
- 一张表：「闭包捕获同一个变量」与「迭代器被消耗」在四门语言里分别在编译期、运行期还是静默地出现。
- 为数据流水线写一条规则，保证第二次遍历不会悄悄变空。

**评分要点**
- Python 输出 `[2, 2, 2]`：闭包捕获的是变量 `i` 本身（晚绑定），循环结束时 `i` 是 2。修复写法是默认参数 `lambda i=i: i`，输出 `[0, 1, 2]`，或者用 `functools.partial` / 工厂函数 ([[pl-functional-closures-pitfall-late-binding-loop]], [[pl-functional-closures-foundation-python-cells]])。
- Go 在 `go 1.22` 下输出 `0 1 2`，`go 1.21` 下输出 `3 3 3`：1.22 起 `for` 的每次迭代有自己的变量；同一份源码仅因为 `go.mod` 的版本行不同而语义不同，升级时没有任何编译报错 ([[pl-functional-closures-history-go-loopvar]], [[pl-functional-closures-foundation-go-shared-variable]])。
- Java 编译失败：`local variables referenced from a lambda expression must be final or effectively final`。Java 用语言规则直接禁止捕获会变化的局部变量，需要计数时只能用 `int[]` 或 `AtomicInteger` 这样的可变容器 ([[pl-functional-closures-foundation-java-effectively-final]])。
- Rust 的 `move || i` 把每次迭代的 `i` 复制进各自的闭包，输出 `[0, 1, 2]`；闭包按用法分成 `Fn`、`FnMut`、`FnOnce`，捕获方式由编译器按使用推出，借用冲突是编译错误 ([[pl-functional-closures-foundation-rust-fn-traits]], [[pl-functional-closures-unique-rust-fn-hierarchy]])。
- 迭代器被消耗：Python 的生成器第二次得到 `[]`（`[0, 1, 4] []`），静默变空；Java 的 `Stream` 第二次抛 `IllegalStateException: stream has already been operated upon or closed`，运行时报错；Rust 的 `collect` 取得迭代器所有权，第二次使用是编译错误 `use of moved value: it`；Go 的 `iter.Seq` 本质是函数，每次 `range` 都重新执行一遍，输出两次 `[start] 0 1 4` ([[pl-functional-iterators-laziness-pitfall-single-use]], [[pl-functional-iterators-laziness-foundation-java-streams]], [[pl-functional-iterators-laziness-unique-go-push-iterators]])。
- 暴露时机：Rust 在编译期，Java 在编译期（捕获）和运行期（流），Go 在语言版本里，Python 全部静默。静默的那个最需要规则与测试兜底 ([[pl-functional-iterators-laziness-table]], [[pl-functional-closures-table]])。
- 流水线规则：需要多次遍历就物化成列表或元组，或者把产生迭代器的函数传下去而不是迭代器本身；对 Python 生成器，在接口文档里写明「只能消费一次」，并用类型注解区分 `Iterator` 与 `Iterable` ([[pl-functional-generators-pitfall-lazy-generator]], [[pl-functional-iterators-laziness-best-practice]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
