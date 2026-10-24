---
id: pl-types-nominal-structural-pitfall-go-pointer-receiver
node: types.nominal-structural
type: qa
step: 6
---
## Q
Go 的隐式接口有什么典型的坑？为什么方法定义在指针上时，值类型不满足接口，该怎么提前发现？

## A
隐式接口的第一个坑：满足关系没有声明，写错了也没有地方报错，要等到你把它赋给接口的那一刻才发现。

第二个坑是方法接收者。方法 `func (d *Dog) Speak()` 属于类型 `*Dog` 的方法集，而 `Dog` 值的方法集里没有它。所以：

```go
type Dog struct{}
func (d *Dog) Speak() string { return "woof" }

var s Speaker = Dog{}   // 编译错误
```

实际错误：

```console
cannot use Dog{} (value of struct type Dog) as Speaker value in variable declaration:
Dog does not implement Speaker (method Speak has pointer receiver)
```

修正是传 `&Dog{}`。

提前发现的惯用法是写一行编译期断言，放在类型定义旁边：

```go
var _ Speaker = (*Dog)(nil)   // 不满足时，包一编译就报错
```

这条语句不产生运行时开销，只是让「Dog 应当实现 Speaker」这个意图变成可检查的声明。如果以后有人删掉或改了 `Speak`，编译立即失败，而不是等到别的包使用时才失败。这等于在结构类型里手动加回名义类型的一点好处。
