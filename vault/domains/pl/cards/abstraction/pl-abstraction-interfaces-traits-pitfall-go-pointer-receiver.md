---
id: pl-abstraction-interfaces-traits-pitfall-go-pointer-receiver
node: abstraction.interfaces-traits
type: qa
step: 9
---
## Q
Go 里一个类型明明有接口要求的方法，却报「does not implement」，常见原因是什么？

## A
Go 的方法有**值接收者**和**指针接收者**两种写法。规则：类型 `T` 的方法集只包含值接收者的方法，`*T` 的方法集包含两种。接口满足要看方法集，所以指针接收者的方法，只有 `*T` 满足接口，`T` 不满足。

```go
type Saver interface{ Save() }
type Doc struct{ n int }
func (d *Doc) Save() { d.n++ }       // 指针接收者
var s Saver = Doc{}
// error: Doc does not implement Saver (method Save has pointer receiver)
```

改成 `var s Saver = &Doc{}` 就能编译，之后两次 `s.Save()` 输出 `saved 1`、`saved 2`，状态保留在同一个对象里。

编译器为什么要这么严格：把 `Doc` 值放进接口，接口里存的是副本。若允许值满足指针接收者的接口，`Save()` 修改的是副本，原对象不变，是一个极难发现的静默错误。Go 选择让它在编译期失败。

实践：同一个类型的方法要么全用指针接收者，要么全用值接收者，不要混用；只要有一个方法需要修改状态或类型较大，就全部用指针接收者，并总是以 `*T` 的形式传递和满足接口。这也是 Go 里隐式满足的一个对应代价：满足关系只在使用点才被检查，错误出现在赋值处而不是定义处。
