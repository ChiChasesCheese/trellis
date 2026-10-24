---
id: pl-meta-codegen-intro-rust-build-rs
node: metaprogramming.code-generation
type: qa
step: 4
---
## Q
Rust 的 `build.rs` 是什么？它和过程宏一样都在编译期生成代码，二者的分工是什么？

## A
**是什么**：Cargo（Rust 的包管理与构建工具）约定：包的根目录里如果有 `build.rs`，Cargo 会先把它当成一个独立的小程序编译并运行，然后才编译包本身。它能做任意事情：生成源文件、编译 C 库、探测系统环境，并通过标准输出向 Cargo 发出指令，如 `cargo::rerun-if-changed=路径`（哪些文件变了才需要重跑）。

**心智模型**：构建前的脚本，但用 Rust 写，并且被 Cargo 缓存管理。它把输出放在环境变量 `OUT_DIR` 指向的目录，主代码用 `include!` 把生成的文件引进来。

**场景**：

```rust
// build.rs
let out = Path::new(&env::var("OUT_DIR").unwrap()).join("gen.rs");
fs::write(out, "pub const N: usize = 3;").unwrap();
// src/main.rs
include!(concat!(env!("OUT_DIR"), "/gen.rs"));
fn main() { println!("N={N}"); }
```

真实输出：`N=3`。常数 `N` 在源码里没有定义，是构建脚本生成的。

**与过程宏的分工**：
- 过程宏**改写某个条目的代码**，输入是语法树片段，出现在用户代码的具体位置。
- `build.rs` **在整个包之外**生成文件或做环境准备，输入是文件系统和环境，典型用途是从 `.proto` 生成代码（prost）、绑定 C 库（bindgen）、读 `schema.json`。

**要记住的一点**：生成的文件默认在 `target/` 里，不进版本库；这是 Rust 与 Go 的约定差别。
