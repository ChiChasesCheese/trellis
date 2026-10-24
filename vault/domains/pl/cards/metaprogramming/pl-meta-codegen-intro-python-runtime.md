---
id: pl-meta-codegen-intro-python-runtime
node: metaprogramming.code-generation
type: qa
step: 5
---
## Q
Python 的 `dataclass` 和元类（metaclass）是怎样在运行时生成代码的？`dataclass` 到底做了什么？

## A
**核心事实**：Python 中，类是在运行时执行 `class` 语句才创建的对象，而且 Python 有 `exec`，能把一段字符串当源码编译执行。所以「生成代码」不需要独立的构建步骤，在你 `import` 一个模块的那一刻就能发生。

**`dataclass` 做了什么**：`@dataclass` 是一个类装饰器。它读取类上带类型注解的字段，把 `__init__`、`__repr__`、`__eq__` 的源码拼成字符串，用 `exec` 编译，再安装到类上。

```python
@dataclass
class P:
    x: int
    y: int
# P.__init__.__code__.co_filename  ->  '<string>'
# P.__init__.__code__.co_varnames  ->  ('self', 'x', 'y')
```

真实输出里文件名是 `<string>`，说明这个 `__init__` 来自一段字符串，而不是任何 `.py` 文件。你得到的效果和手写 `__init__(self, x, y)` 完全一致。

**元类（metaclass）**是「创建类的类」。类对象本身是由 `type` 创建的，你可以换成自己的元类，在类被创建的那一刻自动登记它、检查它、改写它的属性。更轻量的钩子是 `__init_subclass__`：父类里定义它，每个子类被创建时它就自动调用，常用来做插件注册。

**要记住的一点**：这种生成发生在导入时，没有产物可审查，也不能提前验证；好处是不需要任何外部工具。成本是每个类的创建要多花编译时间：本机一次测量，创建 1000 个 dataclass 约 65 ms（约 66 微秒一个），而直接用 `type()` 造同样大小的类约 2 微秒一个。
