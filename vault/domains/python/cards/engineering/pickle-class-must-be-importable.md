---
id: pickle-class-must-be-importable
node: engineering.serialization
type: qa
source: python-docs
---
## Q
把一个自定义类的实例 pickle 之后，改名了这个类、或者把它挪到了另一个模块，再去 `unpickle` 之前保存的数据会发生什么？

## A
pickle 保存类实例时不会把整个类定义写进数据里，只记录了类所在的模块路径和类名；反序列化时会按这个记录去 `import` 对应模块并查找同名的类。类被改名或搬到了别的模块后，pickle 数据里记录的路径就找不到对应的类了，`unpickle` 会失败（抛出找不到该名字的错误）。所以类定义必须在 unpickle 时仍然可以从原来的模块路径导入，重命名或移动类是一个会让旧 pickle 数据失效的破坏性变更。
