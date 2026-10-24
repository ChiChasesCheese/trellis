---
id: pl-memory-resource-management-foundation-go
node: memory.resource-management
type: qa
step: 4
---
## Q
Go 的 `defer` 是什么？多个 `defer` 的执行顺序，以及参数在何时求值？

## A
`defer` 后面跟一个函数调用，含义是“登记这次调用，等当前函数返回时再执行”，无论函数是正常返回、提前 `return` 还是发生 panic。同一函数里的多个 `defer` 按**后进先出**执行。**参数在 `defer` 语句执行的那一刻就求值**，不是等到清理时。

```go
for i := 0; i < 3; i++ {
	defer fmt.Println("deferred", i)   // i is captured now
}
fmt.Println("body")
```

```console
body
deferred 2
deferred 1
deferred 0
```

典型用法是紧跟在资源获取之后：

```go
f, err := os.Open(name)
if err != nil { return err }
defer f.Close()          // runs whenever this function returns
```

这样不管后面有多少个 `return`，文件都会被关闭。要点：`defer` 的作用域是**函数**而不是代码块，所以在循环里 `defer` 要等整个函数结束才执行；Go 的 `defer` 也可以配合命名返回值修改最终结果。

要记住的一个事实：`defer` 轻量、显式，获取与释放写在相邻两行，但调用者必须记得写。
