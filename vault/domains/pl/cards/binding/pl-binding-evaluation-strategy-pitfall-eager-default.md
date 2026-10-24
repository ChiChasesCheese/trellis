---
id: pl-binding-evaluation-strategy-pitfall-eager-default
node: binding.evaluation-strategy
type: qa
step: 10
---
## Q
`Optional.orElse(load())` 和 Rust 的 `unwrap_or(d())` 为什么会在根本用不上缺省值时仍然执行昂贵的计算？

## A
因为参数默认**严格求值**：写在括号里的表达式在调用之前就已经执行了，与被调用的函数是否使用它无关。看上去是「缺省值」，实际是一次必定发生的计算。

Java：

```java
Optional<String> o = Optional.of("x");
o.orElse(load());          // prints "loading default", returns x
o.orElseGet(E::load);      // prints nothing, returns x
```

`orElse(load())` 先调用 `load()`（可能是读数据库、发 RPC），再把结果传给 `orElse`，而 `o` 里明明有值。`orElseGet` 接收的是 `Supplier`，只有在 `o` 为空时才调用。

Rust 的同一对 API：

```rust
fn d() -> i32 { println!("default computed"); 0 }
let o = Some(1);
o.unwrap_or(d());        // prints "default computed", returns 1
o.unwrap_or_else(d);     // prints nothing, returns 1
```

Python 的日志有同样的坑，只是形式不同：`logging.debug(f"v={obj}")` 的 f-string 在调用 `debug` 之前就格式化了，即使日志级别是 WARNING、这条日志根本不会输出，`obj.__str__` 也照样执行（实测会打印一次 `formatted`）；而 `logging.debug("v=%s", obj)` 把格式化推迟到确认要输出时，什么也不执行。

后果：吞吐和延迟被「不会用到的缺省值」拖累；更糟的是缺省值有副作用时（写日志、发请求、创建连接）会产生莫名其妙的行为，比如缓存命中却仍然查了一次数据库。

对策：缺省值的构造不便宜、不纯，就用延迟版本：`orElseGet`、`unwrap_or_else`，或者直接写成 `if` 分支。用 linter 兜底：Rust 的 clippy `or_fun_call`，Python 的 ruff `G004`（日志中使用 f-string）。
