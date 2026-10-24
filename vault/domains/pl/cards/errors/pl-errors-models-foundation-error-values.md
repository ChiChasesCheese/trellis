---
id: pl-errors-models-foundation-error-values
node: errors.models
type: qa
step: 3
---
## Q
Go 的错误返回值是什么样？“多返回值加 `if err != nil`”怎么读？

## A
Go 的函数可以返回多个值。可能失败的函数约定把 `error` 作为**最后一个返回值**：成功时它是 `nil`（“没有错误”），失败时是一个描述错误的值。调用者必须在调用点自己检查：

```go
n, err := strconv.Atoi("12x")
if err != nil {
	fmt.Println("bad:", err)   // bad: strconv.Atoi: parsing "12x": invalid syntax
	return
}
fmt.Println(n)
```

`error` 是一个只有一个方法 `Error() string` 的接口（interface，“一组方法的约定”，任何类型只要有这个方法就算实现了它），所以错误就是普通的值：可以存起来、比较、包装、传给别的函数。控制流没有任何特殊跳转，错误处理就是普通的 `if`。

编译器**不强制**检查：写成 `n, _ := strconv.Atoi("12x")` 把错误丢掉，程序照样编译，`n` 得到零值 0，`go vet` 也不报警。

要记住的一个事实：Go 把错误当作普通返回值，显式、可见，但是否处理完全取决于程序员。
