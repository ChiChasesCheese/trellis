---
id: pl-testing-found-pytest
node: engineering.testing
type: qa
step: 3
---
## Q
pytest 的断言改写（assertion rewriting）、fixture 和 `parametrize` 各解决什么问题？为什么这套「魔法」在 Python 里行得通？

## A
Python 自带 `unittest`（xUnit 风格：继承 `TestCase`，调用 `self.assertEqual`）。pytest 的思路是：测试就是普通函数，直接写裸 `assert`。

1. **断言改写**：pytest 在导入测试模块时改写语法树，把 `assert a == b` 编译成会保留中间值的版本。失败时自动展示两边的值和差异，所以不需要 `assertEqual` 一族：

```text
>   assert slug(raw) == want
E   AssertionError: assert 'a--b' == 'a-b'
E     - a-b
E     + a--b
```

2. **fixture**：测试函数用参数名声明依赖（临时目录、数据库连接、客户端），pytest 按名字注入。fixture 有作用域（函数、模块、整个会话），用 `yield` 之后的代码做清理。这是测试的依赖注入，让准备与清理和测试主体分离。
3. **`@pytest.mark.parametrize`**：一个测试函数加多组参数，展开成多个独立用例，用例名形如 `test_slug[a  b-a-b]`。这是表驱动的 Python 版本。

**为什么行得通**：Python 是动态语言，导入机制允许在模块加载时改写代码，对象的属性也可以在运行时替换（`monkeypatch` 的基础）。框架因此敢于把魔法放进工具里，换取最短的测试代码。

**代价**：魔法需要学习；断言改写只作用于测试模块，辅助模块里的 `assert` 默认得不到详细信息（要用 `register_assert_rewrite` 注册）；fixture 靠名字隐式注入，在大项目里追踪来源比读普通函数调用难。
