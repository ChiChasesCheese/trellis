---
id: pl-errors-error-values-philosophy
node: errors.error-values
type: qa
step: 5
---
## Q
Go 社区说「不要只是检查错误，要优雅地处理它们」，这反映了 Go 错误处理背后怎样的哲学？

## A
Go 的错误处理哲学可以归纳成三句话：

1. **错误是程序正常的一部分。** 打开不存在的文件、解析非法输入，这些不是「异常」，而是会经常发生、需要认真对待的情形，应该用最平常的代码路径处理。
2. **显式胜于简洁。** 每个失败点都写出来，代码读起来是线性的，没有隐式的跳转。让阅读者在每一行都知道「这里可能失败，失败后函数会这样退出」。
3. **错误是数据，可以编程。** Rob Pike 在一篇文章里举了例子：把「写入时累积错误」的逻辑封装到一个类型里，后续的每次写入先检查是否已经出错，这样调用方不必在每一行都写 `if err != nil`。既然是值，就可以设计抽象来化简。

```go
// errWriter remembers the first error; later writes become no-ops
type errWriter struct { w io.Writer; err error }
func (e *errWriter) write(b []byte) {
	if e.err == nil { _, e.err = e.w.Write(b) }
}
```

这与 Rust 形成有趣的对比：同样主张「错误是值」，Rust 相信**类型系统加语法糖**（`Result`、`?`）能同时获得显式和简洁；Go 相信**简单的语言加约定**（`if err != nil`）就够用，并且十多年里多次拒绝了为错误处理引入新语法的提案（如 2019 年的 `try` 提案），原因是新语法会掩盖显式的控制流这一核心优点，且收益有限。

结论：Go 的做法体现的是一种工程取向——语言越小越好，重复的样板是可接受的代价，因为可读性和一致性比简洁更重要。
