---
id: pl-types-numbers-pitfall-rust-profile
node: types.numbers
type: qa
step: 6
---
## Q
同一段 Rust 代码在 debug 和 release 构建下，整数溢出的行为为什么不同？这在线上会造成什么问题？

## A
Rust 的默认规则是：debug 构建开启溢出检查，溢出时 panic；release 构建（`-O`）默认关闭检查，溢出时回绕。这样做的理由是 debug 用来发现 bug，release 要避免检查的运行时开销。

```rust
let n: u8 = std::env::args().count() as u8 + 254;
println!("{}", n + 1);
```

实际运行：

```console
debug:   thread 'main' panicked at o.rs:3:20:
         attempt to add with overflow
release: 0
```

用 `n = 255`，加 1：debug 版本直接 panic，release 版本静默输出 `0`。

线上后果：测试在 debug 下全绿，或者测试里的数据范围不够大，上线后的 release 二进制里 `255 + 1` 悄悄变成 `0`，没有报错，账目或计数就错了。反过来，如果线上只跑过 release 版本，也从没在 debug 下见过 panic，这类 bug 可能一直隐身。

对策：

- 在 `Cargo.toml` 的 `[profile.release]` 设置 `overflow-checks = true`，为安全牺牲少量速度（金融、协议解析类代码强烈建议）。
- 关键路径显式使用 `checked_*`，让行为不依赖构建配置。
- 在 CI 里同时跑 debug 和 release 的测试。

同样的陷阱在 Java 和 Go 里更隐蔽：它们默认永远回绕，没有任何构建配置能让它们在开发阶段报错。
