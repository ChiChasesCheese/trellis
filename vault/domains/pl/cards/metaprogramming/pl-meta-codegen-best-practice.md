---
id: pl-meta-codegen-best-practice
node: metaprogramming.code-generation
type: qa
step: 9
---
## Q
资深工程师怎样在 Go、Java、Rust、Python 里用代码生成？通用规则是什么，何时破例？

## A
**通用规则**：生成器的输入必须是唯一的事实来源（`.proto`、SQL、一份 schema、一个枚举），生成物不手改，并且有一个机制保证「源头一变，产物必变」。理由是生成代码最大的风险不是出错，而是悄悄过期。

- **Go**：生成物提交入库；在文件头保留 `Code generated ... DO NOT EDIT.`；CI 里先 `go generate ./...` 再 `git diff --exit-code`，不一致就失败。把所有 `//go:generate` 的命令固定版本，不要用 `@latest`，否则不同机器生成的结果不同。
- **Java**：在 Maven 或 Gradle 里把处理器声明为 `annotationProcessor` 依赖，不依赖 IDE 的隐式配置；生成目录加入 `.gitignore`；调试生成的类时，检查生成源码目录。
- **Rust**：`build.rs` 里必须写 `cargo::rerun-if-changed`，不写的话，包内任何文件变化都会重跑脚本；生成逻辑尽量薄，复杂的放在普通库里做单元测试。
- **Python**：不要为了少写几行就写元类；优先 `dataclass`、`typing.NamedTuple` 等标准库；热路径上创建大量类的场景要测量导入时间。

**何时破例**：一次性迁移脚本、原型阶段，手写或临时生成都可以。但只要生成物会长期留在仓库里，就要上述的一致性检查。
