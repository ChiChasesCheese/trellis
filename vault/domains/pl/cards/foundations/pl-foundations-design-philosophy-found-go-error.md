---
id: pl-foundations-design-philosophy-found-go-error
node: foundations.design-philosophy
type: qa
step: 2
---
## Q
Go 的错误处理是什么样的？为什么说「错误是值」，`error` 返回值和 Java 的异常有什么根本区别？

## A
Go 没有异常机制。可能失败的函数多返回一个 `error` 类型的值，约定放在最后；成功时它是 `nil`。调用者自己检查，决定处理还是继续向上返回。`error` 只是一个接口，要求有一个返回字符串的 `Error()` 方法，所以它是普通的值，可以保存、比较、包装、放进 map。

```go
n, err := strconv.Atoi("12x")
if err != nil {
    fmt.Println("failed:", err)
    return
}
fmt.Println(n)
```

实际输出：`failed: strconv.Atoi: parsing "12x": invalid syntax`。

与异常的根本区别是控制流：异常让失败沿着调用栈自动向上跳，中间的函数可以什么都不写；Go 的错误必须在每一层显式处理或转交，代码里每个可能失败的位置都是可见的，不存在看不见的退出路径。代价是重复的 `if err != nil`，好处是读代码时能看清每一步的失败如何处理。

另有 `panic`，保留给真正不可恢复的错误（如数组越界、程序逻辑错误），不用于普通的业务失败。
