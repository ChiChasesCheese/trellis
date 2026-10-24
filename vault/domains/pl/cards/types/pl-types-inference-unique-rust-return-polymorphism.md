---
id: pl-types-inference-unique-rust-return-polymorphism
node: types.inference
type: qa
step: 4
---
## Q
Rust 里同一个方法 `parse()` 为什么能根据你想要的类型返回不同的结果？这种「按返回类型选择实现」的能力 Java、Go、Python 有吗？

## A
Rust 的 `"42".parse()` 本身是泛型方法 `parse::<F>()`，其中 `F` 是要解析成的类型，只要实现了 `FromStr` trait 就行。编译器通过返回值被赋给什么类型来决定 `F`：

```rust
let n: u64 = "42".parse().unwrap();     // F = u64
let f: f64 = "4.5".parse().unwrap();    // F = f64
let w: Vec<i32> = (1..4).collect();     // 收集成 Vec
let t: String = ['a', 'b'].iter().collect();   // 收集成 String，输出 ab
```

同一个 `collect()` 调用，按目标类型能产出 `Vec`、`String`、`HashMap` 等不同容器。这叫返回类型多态（return-type polymorphism）。

如果左边没有给出类型，编译器会报错：

```console
error[E0284]: type annotations needed
  "42".parse().unwrap()  // type must be known at this point
```

此时必须写成 `let n = "42".parse::<u64>()`（turbofish 语法）或者给变量加标注。

Java 做不到：方法重载只看参数类型，不看返回值，所以 `Integer.parseInt`、`Double.parseDouble` 各写一个名字；Go 也靠不同函数名（`strconv.Atoi`、`ParseFloat`）；Python 靠 `int(s)`、`float(s)` 选不同的类型构造函数。Rust 这种能力来自「类型推断加 trait」的组合，代价是出错时的类型推断报错有时令人困惑。
