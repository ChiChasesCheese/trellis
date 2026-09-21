---
id: types-typeddict-dataclass-field-discovery
node: types.typeddict-literal
type: qa
source: python-docs
---
## Q
`@dataclass` 装饰器怎么知道一个类有哪些字段（field）？它会检查注解里写的具体类型吗？

## A
`@dataclass` 扫描类体里「带类型注解的类变量」来确定字段集合，字段在生成的 `__init__`/`__repr__` 等方法里的顺序就是它们在类定义里出现的顺序。除了两个例外（`ClassVar` 标注的变量被当成普通类变量、不生成实例字段；`InitVar` 标注的变量只进构造函数参数、不保留为字段），`@dataclass` 本身并不检查注解里写的具体类型是否正确——这一步和其他类型提示一样，只是静态检查器的工作。
