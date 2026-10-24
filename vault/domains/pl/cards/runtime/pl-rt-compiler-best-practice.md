---
id: pl-rt-compiler-best-practice
node: runtime.compiler-pipeline
type: qa
step: 8
---
## Q
面对编译慢（尤其是 Rust）和构建缓存，资深工程师在日常开发和 CI 里怎么做？

## A
**原则**：把“快速反馈”和“最终产物”分开优化。检查正确性不需要生成优化后的机器码。

**Rust**：
1. 日常用 `cargo check`：只做解析、类型与借用检查，跳过代码生成，比完整构建快数倍。
2. 把项目拆成多个 crate（编译单元）。crate 是 rustc 的并行与缓存粒度，单个巨型 crate 改一行就要重编大部分；依赖与稳定代码单独成 crate。
3. 开发 profile 对依赖开优化，对自己的代码保持低优化：在 `Cargo.toml` 里设 `[profile.dev.package."*"] opt-level = 3`，既保留快速增量编译，又不让依赖库慢得无法测试。
4. 控制泛型与过程宏的使用面；热路径之外用 `dyn Trait`，减少单态化膨胀。
5. CI 里缓存 `target/` 与依赖（`sccache`、`Swatinem/rust-cache`），并使用更快的链接器（`lld`、`mold`）。
6. 发布用 `--release`；需要时再调 LTO（链接期优化，跨 crate 内联）与 `codegen-units=1`，换更小更快的二进制，代价是更慢的构建。

**C++**：慢在头文件重复解析和模板实例化，而不是优化。用 ccache（按编译输入缓存目标文件）加并行的 Ninja；头文件里只放声明、用前置声明（forward declaration）减少 `#include`；大模板移到 `.cpp` 里显式实例化；预编译头和 C++20 模块进一步削减；用 Clang 的 `-ftime-trace` 找最慢的头文件和模板。

**Go**：构建本来就快，关键是别破坏缓存：保持稳定的包边界，构建缓存放进 CI；用 `go build -race` 之类只在需要时。

**Java**：用 Gradle / Maven 的增量编译与构建缓存；注解处理器会拖慢编译，要审视它的必要性。

**Python**：没有编译步骤可优化，但要让 `.pyc` 缓存生效（只读文件系统上预先生成），并避免在导入时执行重工作。

**通用**：把编译时间当作预算来度量（Rust 用 `cargo build --timings`），在 PR 里监控，一旦回归就找原因，而不是等到大家都抱怨。
