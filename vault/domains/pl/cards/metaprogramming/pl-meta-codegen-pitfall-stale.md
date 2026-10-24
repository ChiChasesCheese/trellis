---
id: pl-meta-codegen-pitfall-stale
node: metaprogramming.code-generation
type: qa
step: 10
---
## Q
Go 里生成的代码过期会怎样？为什么它不会被编译器拦下，线上表现是什么？

## A
`go build` 不会自动运行 `go generate`。如果你给枚举加了一个值却忘记重新生成，旧的生成文件依然是合法的 Go 代码，编译照样通过。

```go
const ( Red Color = iota; Green; Blue; Yellow )   // Yellow added, not regenerated
fmt.Println(Red, Blue, Yellow)
```

真实输出：`Red Blue Color(3)`。`stringer` 生成的 `String()` 对不认识的值回退为 `Color(3)`，没有 panic，没有编译错误，日志和 API 响应里直接出现 `Color(3)`。

`stringer` 其实在生成文件里放了一道防线：文件里有 `_ = x[Red-0]` 这类语句，如果常量的值被改动，会产生「invalid array index」的编译错误。但**新增**常量并不会触发它，新增是最常见的变更，所以防线形同虚设。

**更普遍的失败模式**：`.proto` 改了没重新生成，客户端静默忽略新字段；SQL 改了没重新生成，运行时才报错。

**防线**：
1. CI 里 `go generate ./... && git diff --exit-code`，不同步就失败。
2. 把生成命令放进 `Makefile` 或 `just` 任务，作为 `build` 的前置。
3. 对枚举写一个测试，遍历所有值断言名字不以 `Color(` 开头。

原则：所有「靠人记得运行」的步骤，最终都会被忘；要么自动化，要么用 CI 强制。
