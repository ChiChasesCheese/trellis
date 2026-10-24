---
id: pl-abstraction-composition-embedding-mechanism
node: abstraction.composition-embedding
type: qa
step: 5
---
## Q
Go 的嵌入和 Java 的继承在「方法内部的 self」上有什么本质区别？一个小例子会输出什么？

## A
关键区别：**被嵌入类型的方法里，接收者是被嵌入的那个对象，不是外层**。Go 的嵌入没有「虚方法」，不会回调外层的覆盖版本。

```go
type Base struct{}
func (b Base) Name() string  { return "base" }
func (b Base) Greet() string { return "hello from " + b.Name() }
type Child struct{ Base }
func (c Child) Name() string { return "child" }
fmt.Println(Child{}.Greet())   // 输出：hello from base
```

```java
class Base { String name() { return "base"; } String greet() { return "hello from " + name(); } }
class Child extends Base { @Override String name() { return "child"; } }
System.out.println(new Child().greet());   // 输出：hello from child
```

Java 的 `greet()` 里 `this.name()` 是虚调用，`this` 是 `Child`，所以取到覆写版本。Go 的 `Greet` 里 `b` 就是一个 `Base` 值，它的 `b.Name()` 在编译期就绑定到 `Base.Name`。

C++ 把这个选择交给 `virtual`：
```cpp
std::string name() const { return "base"; }                 // non-virtual
virtual std::string vname() const { return "base"; }
std::string greet()  const { return "hello from " + name(); }
std::string vgreet() const { return "hello from " + vname(); }
// Child redefines both name and vname:  prints "hello from base | hello from child"
```
本机实际输出 `hello from base | hello from child`：非虚函数像 Go，在 `Base` 里就绑定到 `Base::name`；`virtual` 函数像 Java，调用到派生类的覆写。
这解释了嵌入「更安全」的原因：被嵌入类型的行为不会被外层悄悄改变（没有脆弱基类问题），也解释了它「做不到」什么：经典的模板方法模式（父类写骨架、子类填空）在 Go 里要换写法，把「填空的部分」作为接口或函数参数显式传进去。
