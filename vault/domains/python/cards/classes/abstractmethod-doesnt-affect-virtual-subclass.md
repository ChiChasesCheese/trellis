---
id: abstractmethod-doesnt-affect-virtual-subclass
node: classes.abc-protocols
type: qa
source: python-docs
---
## Q
一个类通过 `SomeABC.register()` 被注册为虚拟子类之后，`SomeABC` 里用 `@abstractmethod` 标记的方法还会不会强制它必须实现？

## A
不会。`@abstractmethod` 造成的『必须重写才能实例化』这条限制，只对通过常规继承（`class C(SomeABC)`）得到的子类生效；通过 `register()` 注册的虚拟子类完全不受影响——即使它一个抽象方法都没实现，也照样能被实例化，`isinstance()`/`issubclass()` 照样返回 `True`。这是「虚拟子类」这个机制的本质：它只影响类型检查的结果，不接入继承链，也不接入 ABC 的强制校验。
