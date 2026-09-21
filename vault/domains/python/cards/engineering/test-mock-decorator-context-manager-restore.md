---
id: test-mock-decorator-context-manager-restore
node: engineering.testing
type: qa
source: python-docs
---
## Q
用 `@patch('module.ClassName')` 装饰测试函数，或者用 `with patch.object(...) as m:` 作为上下文管理器，打桩的对象在什么时候会被恢复成原来的值？

## A
两种用法效果一致：`patch()` 只在被装饰的测试函数运行期间（decorator 形式）或 `with` 代码块内（context manager 形式）临时替换目标对象；测试函数返回或 `with` 块结束时，无论测试是否抛出异常，原始对象都会被自动恢复，不会污染后续的测试或代码。
