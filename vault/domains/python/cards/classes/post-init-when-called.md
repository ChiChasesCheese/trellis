---
id: post-init-when-called
node: classes.dataclasses
type: qa
source: python-docs
---
## Q
`__post_init__()` 是什么时候被调用的？它的典型用途是什么，跟 `InitVar` 有什么关系？

## A
如果类定义了 `__post_init__()`，dataclass 生成的 `__init__()` 会在给所有字段赋值完之后，自动调用一次 `self.__post_init__()`——若没有生成 `__init__()`（比如自己手写了），`__post_init__()` 就不会被自动调用。典型用途是做跨字段校验或计算派生字段（比如 `c` 由 `a + b` 算出）。若类里有用 `InitVar[T]` 标注的伪字段，它们不会成为真正的实例属性，只会被当作参数传进 `__init__()` 和 `__post_init__()`，按声明顺序排在其余字段后面传入。
