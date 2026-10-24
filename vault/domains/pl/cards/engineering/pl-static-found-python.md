---
id: pl-static-found-python
node: engineering.static-analysis
type: qa
step: 5
---
## Q
Python 里 mypy 和 ruff 分别做什么？在一门没有强制类型的语言里，静态分析的位置有什么不同？

## A
Python 在运行时才检查类型，类型注解对解释器不起任何作用（运行时忽略），所以静态分析是**可选的、由工具外挂的**：
- **类型检查器**（mypy、pyright）：读取你写的注解，检查调用和返回值是否一致。这是**渐进类型**（gradual typing）：有注解的部分被检查，没注解的部分当作 `Any` 放过。
- **ruff**：用 Rust 写的 linter，实现了 flake8、isort、pyupgrade 等一大批规则，速度比老工具快一到两个数量级，因此可以在编辑器里保存即检查。它还能自动修复一部分问题。

**例**：

```python
import os                          # unused

def load(path: str) -> int:
    try:
        return open(path).read()   # returns str, annotated int
    except:                        # bare except
        pass

def add(items=[]):                 # mutable default
    items.append(1)
    return items
```

这段代码能 `import`，运行不报错。`ruff check --select F,E7,B` 的输出：

```text
F401 [*] `os` imported but unused
E722 Do not use bare `except`
B006 Do not use mutable data structures for argument defaults
```

`mypy` 的输出：

```text
a.py:3: error: Missing return statement  [return]
a.py:5: error: Incompatible return value type (got "str", expected "int")  [return-value]
```

分工清晰：ruff 抓的是写法层面的陷阱（`B006` 默认值是同一个列表对象，会在调用之间共享），mypy 抓的是类型不一致。

**对比**：Go、Rust、Java 的类型检查是编译器的一部分，没得选；Python 的保证强度取决于团队愿意写多少注解、是否把检查放进 CI。所以在 Python 里，静态分析的投入比例最高。
