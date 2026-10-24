---
id: pl-types-nominal-structural-found-go-implicit-interface
node: types.nominal-structural
type: qa
step: 3
---
## Q
Go 的接口为什么不需要 `implements`？类型「隐式满足」接口是什么意思？

## A
Go 的接口也是一组方法签名。区别是：类型不需要声明自己实现了哪个接口，只要它的方法集（method set，即这个类型拥有的全部方法）包含了接口要求的每个方法，且名字、参数、返回值都一致，它就自动满足这个接口。

```go
type Flyer interface{ Fly() string }
type Bird struct{}
func (Bird) Fly() string { return "flap" }

var f Flyer = Bird{}   // Bird 的定义里从未出现 Flyer
fmt.Println(f.Fly())   // flap
```

实际输出 `flap`。`Bird` 的代码和 `Flyer` 的定义可以在不同的包里，彼此互不知晓。

这意味着接口可以由使用方事后定义：你要写一个函数，只需要对象能 `Fly`，就在自己的包里写一个只有 `Fly` 的小接口，别人已有的类型自动适用，不用修改它们。这就是结构类型（structural typing）：兼容关系取决于类型的「形状」（有哪些方法），而不是名字。

隐式满足有一个细节：一个接口变量内部同时记录具体类型和值，调用方法时按具体类型的方法查找。所以满足是编译期检查的，但是看一个类型的定义，找不到它实现了哪些接口。
