---
id: pl-meta-reflection-intro-python
node: metaprogramming.reflection
type: qa
step: 4
---
## Q
Python 的内省（introspection）是什么？为什么它不需要一套单独的「反射 API」，`getattr`、`dir`、`inspect` 怎样在具体场景中工作？

## A
**是什么**：Python 里一切都是对象，每个普通对象有一个字典 `__dict__` 保存它的属性，每个对象有一个 `type`，类本身也是对象。所以「查看和操作对象的结构」不是特殊能力，而是语言原本的数据模型，内置函数就是它的入口。

**心智模型**：对象是一个「名字到值」的字典；`obj.name` 只是 `getattr(obj, "name")` 的语法糖，区别仅仅是名字写死在源码里还是运行时传入。

```python
class User:
    def __init__(self): self.name = "ann"
    def greet(self, who): return f"hi {who}, I am {self.name}"
u = User()
print(u.__dict__)                       # {'name': 'ann'}
print(getattr(u, "greet")("bob"))       # hi bob, I am ann
setattr(u, "age", 30)                   # {'name': 'ann', 'age': 30}
print(hasattr(u, "nope"))               # False
```

上面是真实输出。`dir(u)` 列出对象与其类上所有可用名字，`inspect.signature(User.greet)` 得到 `(self, who)`，`type(u).__name__` 得到 `User`。

**要记住的一点**：因为方法、字段、类在运行时都可以被读写甚至替换，Python 的框架（Django 的模型、pytest 的 fixture、Flask 的路由）可以几乎不用任何注册代码，扫描一个模块里的对象就完成装配。代价是类型检查工具很难知道某个名字到底存不存在。
