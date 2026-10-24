---
id: pl-foundations-paradigms-found-go-struct-method
node: foundations.paradigms
type: qa
step: 3
---
## Q
Go 没有 `class`，它怎样把数据和行为绑在一起？方法的接收者（receiver）是什么？

## A
Go 把「数据」和「行为」分开声明：`struct` 只声明字段，方法则是在类型外面单独写的函数，只是在函数名前多了一个接收者参数。接收者写在 `func` 和方法名之间，相当于 Java 里隐含的 `this`，但你可以自己命名并选择它是值还是指针。

```go
type Counter struct{ n int }

func (c *Counter) Inc()    { c.n++ }   // 指针接收者：改的是原对象
func (c Counter) IncCopy() { c.n++ }   // 值接收者：改的是副本

c := Counter{}
c.Inc()
c.IncCopy()
fmt.Println(c.n)   // 1
```

实际输出 `1`：`Inc` 改了原对象，`IncCopy` 操作的是调用时复制出的副本，改动随副本消失。

要点：Go 里任何自己定义的具名类型（不只是 `struct`）都可以有方法；方法只是语法糖，`c.Inc()` 等价于把 `&c` 作为第一个参数传给 `Inc`。没有继承，没有构造函数关键字（惯例是写一个返回结构体的 `NewX` 函数）。「谁有哪些方法」决定了这个类型能满足哪些接口，这是 Go 面向对象的全部基础。
