---
id: pl-binding-evaluation-strategy-foundation-iterators
node: binding.evaluation-strategy
type: qa
step: 5
---
## Q
Python 的生成器（generator）和 Rust 的迭代器适配器怎样实现惰性？什么时候计算真正发生？

## A
两者都把「怎么产生下一个元素」封装成一个对象，**消费者每要一个才算一个**。

**Python 生成器**：函数体里出现 `yield`，调用它不执行函数体，只返回生成器对象。每次 `next()` 才运行到下一个 `yield` 暂停，保留所有局部变量：

```python
def gen():
    for i in range(3):
        print("produce", i); yield i
g = gen(); print("created")   # created  (nothing produced yet)
print(next(g))                # produce 0, then 0
```

组合起来可以处理无限序列：`itertools.islice((x*x for x in itertools.count()), 4)` 得到 `[0, 1, 4, 9]`，永远不会把「所有平方数」算出来。生成器表达式 `(… for …)` 同理。

**Rust 迭代器**：`Iterator` 是一个有 `next()` 方法的 trait；`map`、`filter`、`take` 这类适配器返回新的迭代器结构体，**什么都不执行**，直到 `collect`、`sum`、`for` 循环去拉数据：

```rust
let it = (1..4).map(|x| { println!("map {x}"); x * 2 });
println!("built");              // built
let v: Vec<i32> = it.collect(); // map 1, map 2, map 3
```

输出顺序是 `built`、`map 1`、`map 2`、`map 3`。适配器链会被编译器内联成一个循环，没有中间集合，所以惰性在 Rust 里是零成本的；Rust 对此还标了 `#[must_use]`：只构造不消费会得到编译警告，因为那等于什么都没做。

Go 没有内建的惰性序列，通道（channel）加协程能模拟但代价高；1.23 起标准库增加了 `iter.Seq`，用「回调式迭代 + `range` 过 func」实现惰性，`break` 会让生产者停下。

共同点：惰性靠**拉模型**（pull）实现，由消费者驱动。要记住的事实：第一次真正读取元素之前，什么都没有发生。
