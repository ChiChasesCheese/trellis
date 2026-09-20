---
id: python-modules-type-checking-guard
node: python.modules
type: qa
step: 6
tags: [grown]
---
## Q
`if TYPE_CHECKING: import b` 这种写法解决了什么问题？和直接在函数体内延迟 `import b` 有什么不同？

## A
当 `a.py` 只是想在类型注解里引用 `b` 模块的类型（比如 `def handle(order: "b.Order") -> None`），并不需要在**运行时**真的拿到 `b` 模块，这种引用完全可以打破循环导入而不牺牲类型检查：`typing.TYPE_CHECKING` 在运行时永远是 `False`，所以 `import b` 根本不会执行，不会触发循环导入；但类型检查器（mypy）会把它当成 `True` 来解析，注解依然能被正确检查。区别于函数内延迟导入：延迟导入是**运行时真的需要**这个模块（只是推迟加载时机），`TYPE_CHECKING` 守卫的导入**运行时根本不需要**，纯粹是给类型检查器看的。
