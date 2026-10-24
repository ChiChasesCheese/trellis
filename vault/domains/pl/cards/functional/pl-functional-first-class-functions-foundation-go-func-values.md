---
id: pl-functional-first-class-functions-foundation-go-func-values
node: functional.first-class-functions
type: qa
step: 3
---
## Q
Go 的函数值是什么？函数类型怎样匹配，「函数选项模式」为什么成为惯用法？

## A
Go 的函数是一等值，有内置的**函数类型**：`func(int) int`。类型相同当且仅当参数和返回值类型相同（结构化匹配，不需要声明接口），函数字面量可以直接赋值、传递、返回，并且能引用外层变量（闭包）。实测一个函数值占 8 字节（一个指向代码和捕获变量的指针）。

最典型的惯用法是**函数选项**（functional options）：用函数类型表达「对配置对象的一次修改」。

```go
type Server struct{ port int; tls bool }
type Option func(*Server)
func WithPort(p int) Option { return func(s *Server) { s.port = p } }
func New(opts ...Option) *Server {
    s := &Server{port: 80}
    for _, o := range opts { o(s) }
    return s
}
New(WithPort(8080))   // &{8080 false}
```

为什么选它：Go 没有重载、没有默认参数、没有命名参数。构造函数要支持「可选配置、将来可扩展、调用方简洁」，用 `New(opts ...Option)` 就实现了：新增选项只需新增一个函数，不会破坏已有调用；零个选项时是默认值；选项还可以带校验。

这是 Go 用最少的语言特性（函数值 + 可变参数）解决其他语言用构造器重载、Builder、命名参数解决的问题，体现了 Go 的取向：靠组合简单机制，而不是增加语法。
