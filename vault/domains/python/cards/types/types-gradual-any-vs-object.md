---
id: types-gradual-any-vs-object
node: types.gradual-typing
type: qa
source: python-docs
---
## Q
面试官常问：类型标注里 `Any` 和 `object` 有什么区别？

## A
用 `object` 标注表示值可以是任意类型，但检查器仍严格检查——对 `object` 类型的值几乎不能做任何操作，把它赋给更具体类型的变量也是类型错误，因为 `object` 虽是所有类型的父类，反过来却不是所有类型的子类。用 `Any` 标注则是关闭类型检查的逃生舱（escape hatch）——`Any` 可赋值给任意类型、也接受任意类型赋值，对 `Any` 值调用任意方法都能通过检查，代价是彻底放弃了对这段代码的静态保障。
