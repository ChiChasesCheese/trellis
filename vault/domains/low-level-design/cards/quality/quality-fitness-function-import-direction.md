---
id: quality-fitness-function-import-direction
node: quality.fitness-functions
type: qa
step: 2
---
## Q
写一个适应度函数,检查 `domain` 包里的模块不允许 import `infrastructure` 包（依赖只能从外层指向内层）。用 `ast` 怎么实现？

## A
```python
import ast
from pathlib import Path

def imports_of(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        elif isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
    return names

def test_domain_does_not_import_infrastructure():
    for path in Path("src/domain").rglob("*.py"):
        bad = {n for n in imports_of(path) if n.startswith("infrastructure")}
        assert not bad, f"{path} imports {bad}"
```
用 `ast.parse` 而不是 `import` 这些模块本身来检查，是因为只想读它们**声明了哪些依赖**，不需要（也不应该）真的执行这些模块的代码——静态分析比动态导入更快、更安全，也不会因为某个模块导入时有副作用而出问题。
