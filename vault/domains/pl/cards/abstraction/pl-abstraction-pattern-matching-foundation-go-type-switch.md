---
id: pl-abstraction-pattern-matching-foundation-go-type-switch
node: abstraction.pattern-matching
type: qa
step: 5
---
## Q
Go 的 type switch 能做什么、不能做什么？为什么说它只是模式匹配的一半？

## A
Go 没有模式匹配，最接近的是 **type switch**：对一个接口值，按它的**动态类型**分支，并在分支里得到该类型的变量。

```go
func area(s Shape) float64 {      // Shape 是空接口 interface{}
    switch v := s.(type) {
    case Circle: return 3 * v.R * v.R
    case Rect:   return v.W * v.H
    }
    return -1
}
area(Circle{1})      // 3
area(struct{}{})     // -1：没匹配上，静默走到默认值
```

它只做到了模式匹配的**一半**：

- ✔ 判断形态，并取得带类型的变量。
- ✘ **不能解构**：不能在模式里写 `Rect{W: 0, H: h}`；字段要在分支里手动取。
- ✘ **不能嵌套**，不能带守卫（要在分支里再写 `if`）。
- ✘ **没有穷尽检查**：接口是开放的，任何类型都能满足，编译器不可能证明「所有情况都处理了」。所以必须自己写一个兜底，或者接受漏掉。

原因是 Go 没有和类型（代数数据类型）：接口是开放的，没有「只有这几种形态」这样的声明。没有封闭集合，穷尽检查就没有意义，复杂的模式也就失去了基础。社区的常用做法是：用接口 + 方法，让每个类型自己定义行为（`s.Area()`），把分支留给确实需要的少数地方；或者在接口里放一个未导出的方法，把实现限制在包内，用作「准封闭」。
