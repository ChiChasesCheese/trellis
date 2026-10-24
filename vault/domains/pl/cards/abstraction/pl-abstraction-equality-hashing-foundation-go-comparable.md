---
id: pl-abstraction-equality-hashing-foundation-go-comparable
node: abstraction.equality-hashing
type: qa
step: 5
---
## Q
Go 的 `==` 对哪些类型有定义？可比较（comparable）类型在 map 键和接口里有什么坑？

## A
Go 的 `==` 由语言**内置**，没有用户重载。规则：基本类型按值比较；数组和结构体在**所有元素 / 字段都可比较**时逐个比较；指针比较地址；接口值比较「动态类型和值」都相同。**切片、map、函数不可比较**（只能和 `nil` 比），含这些的结构体也不可比较。

`comparable` 是内置的泛型约束，表示能用 `==` 的类型，也是 map 键的要求。不可比较的类型当键，编译期拒绝：

```go
_ = map[[]int]string{}
// invalid map key type []int
```

但接口会把这个检查推迟到**运行期**：

```go
var a, b any = []int{1}, []int{1}
fmt.Println(a == b)
// panic: runtime error: comparing uncomparable type []int
```

`any` 在编译期看起来是可比较的，等到两边真的装了切片才 panic。同样，`map[any]V` 用切片做键，也会在运行期 panic。

这套规则的哲学是：相等是一个编译器内置的、永远可预测的操作，不允许用户重载，也不会有隐藏代价。要比较切片，用 `slices.Equal`；要比较复杂结构，用 `reflect.DeepEqual`（慢，且对 `NaN` 等有特殊规则）或手写。取舍是：没有自定义相等，意味着「按 ID 比较两个实体」「忽略大小写」这类需求只能写独立的函数，不能接入 `==` 或 map 键。
