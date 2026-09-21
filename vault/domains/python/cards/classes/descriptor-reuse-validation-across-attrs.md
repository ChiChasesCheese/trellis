---
id: descriptor-reuse-validation-across-attrs
node: classes.properties-descriptors
type: qa
source: python-docs
---
## Q
同一段校验逻辑，写在 `@property` 里 vs 写成独立的描述符类，在「跨多个属性复用」这件事上有什么区别？

## A
用 `@property` 时，每个受管理属性都要单独写一遍 `getter/setter`（哪怕校验逻辑完全一样），因为 property 是绑定到某一个方法名的。把校验逻辑写成一个独立的描述符类（比如 `class Number(Validator)`，内部定义 `__get__`/`__set__`）之后，可以把同一个描述符类实例化多次，分别赋给类里的不同属性名（如 `quantity = Number(minvalue=0)`、`price = Number(minvalue=0)`），每个实例借助 `__set_name__()` 自动知道自己对应哪个属性、该往实例的哪个私有名字里存值，从而把同一份校验逻辑复用到任意多个属性上而不用重复代码。
