---
id: pl-abstraction-polymorphism-kinds-foundation-go-python-structural
node: abstraction.polymorphism-kinds
type: qa
step: 3
---
## Q
Go 的隐式接口和 Python 的鸭子类型（duck typing）分别是什么？它们怎样在不声明继承关系的情况下实现多态？

## A
共同的心智模型：**不问「你声明过自己是什么」，只问「你有没有我要用的那些方法」**。

**Go**：接口是一组方法签名；任何类型只要方法集合包含这些方法，就自动满足它，不需要写 `implements`。

```go
type Stopper interface{ Stop() }
type Timer struct{}
func (Timer) Stop()  { fmt.Println("timer stopped") }
type Engine struct{}
func (Engine) Stop() { fmt.Println("engine stopped") }
func shutdown(s Stopper) { s.Stop() }
// shutdown(Timer{}) 输出 timer stopped；shutdown(Engine{}) 输出 engine stopped
```

`Timer` 的作者从没听说过 `Stopper`，接口甚至可以在多年后由使用方才定义。检查仍在编译期完成：缺方法就编译失败。

**Python**：根本没有声明，调用时直接 `obj.close()`，对象有就行，没有则运行期抛 `AttributeError`。若想让静态工具也能检查，可以写 `Protocol`（一个只描述方法形状的类），效果等同 Go 的隐式接口，但只由 `mypy` 之类的工具检查。Python 没有重载，需要按参数类型选不同实现时用标准库的 `functools.singledispatch`，它在运行期按第一个参数的类型挑选函数。

这两种都是「按形状匹配」的子类型多态，与 Java、Rust 要求事先声明「我实现了 X」的做法相对。
