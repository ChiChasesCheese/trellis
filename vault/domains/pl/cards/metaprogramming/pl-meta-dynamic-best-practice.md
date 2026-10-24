---
id: pl-meta-dynamic-best-practice
node: metaprogramming.dynamic-features
type: qa
step: 9
---
## Q
资深 Python 工程师怎样使用猴子补丁、`__getattr__`、描述符、元类和 `eval`？什么时候该用，什么时候不该用？

## A
**总规则**：用能解决问题的最弱一级。阶梯是：普通函数与类，然后 `property`，然后描述符，然后 `__init_subclass__`，最后才是元类。`eval` 在业务代码里基本不用。越往上一级，越难被同事和工具读懂。

- **猴子补丁**：只在测试里，并且用 `unittest.mock.patch` 或 pytest 的 `monkeypatch` fixture，它们保证作用域结束后还原。生产代码里补丁别人的库，只作为临时热修补，注明升级后删除。
- **`__getattr__`**：只用于代理和动态 API 客户端，必须在入口处限制：对 `_` 开头或不在白名单里的名字立即 `raise AttributeError`，不要什么都返回。
- **描述符**：用来复用「验证/转换/惰性计算」逻辑，同样的 `property` 写到第三个字段时就该提取成描述符；用 `__set_name__` 自动拿到字段名。
- **元类 vs `__init_subclass__`**：能用后者就不用前者。元类会和另一个库的元类冲突，且多数同事没学过。
- **`eval`/`exec`**：永远不接外部输入；解析字面量用 `ast.literal_eval`；需要表达式语言就用成熟的解析器。

**补偿动态性的工具**：加类型注解和 `mypy`/`pyright`；动态属性用 `__getattr__` 时配套写 `.pyi` 存根；把动态逻辑集中在一个小模块，周围代码保持静态。

**何时破例**：框架或库内部。几乎所有流行的 Python 库都在内部用了这些技巧，目的是让**使用者**的代码保持简单、静态。
