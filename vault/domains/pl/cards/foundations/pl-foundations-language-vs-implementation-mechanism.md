---
id: pl-foundations-language-vs-implementation-mechanism
node: foundations.language-vs-implementation
type: qa
step: 4
---
## Q
怎样判断某个行为是「语言特性」还是「实现细节」？CPython 的引用计数导致的哪种行为就属于实现细节？

## A
判断办法只有一条：语言规范有没有保证它。保证了，所有合格的实现都必须这样；没保证，就只是当前这个实现碰巧如此，换个实现、换个版本可能就变。

CPython 靠引用计数管理内存：对象的引用数归零，立刻调用 `__del__` 并释放。

```python
class R:
    def __del__(self):
        print("freed")

r = R()
r = None
print("after")
```

在 CPython 3.14 上实际输出是 `freed`，然后 `after`：赋值 `r = None` 让计数归零，对象当场被销毁。这不是 Python 语言的保证。语言参考明确说不保证对象何时被销毁；PyPy 使用追踪式垃圾回收，`freed` 可能在 `after` 之后很久才出现，甚至程序结束时才出现。

所以「用完对象文件就自动关闭」之类的依赖，写在 CPython 上看起来没问题，换实现就会泄漏文件句柄。规范层的做法是显式管理资源：`with open(...)`。类似的实现细节还有：全局解释器锁（GIL）、小整数缓存、`dict` 的内部布局。
