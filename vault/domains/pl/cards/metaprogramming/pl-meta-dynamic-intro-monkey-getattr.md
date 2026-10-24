---
id: pl-meta-dynamic-intro-monkey-getattr
node: metaprogramming.dynamic-features
type: qa
step: 2
---
## Q
什么是猴子补丁（monkey patching）和 `__getattr__`？它们的心智模型和一个具体场景是什么？

## A
**猴子补丁**：Python 里模块、类、函数都是可以被重新赋值的普通对象，所以运行时可以直接把已有名字指向一个新实现。

```python
import json
orig = json.dumps
json.dumps = lambda *a, **k: "patched"
print(json.dumps({}))      # patched  (every caller of json.dumps is affected)
json.dumps = orig
```

真实输出：`patched`。心智模型：整个进程共用一张「名字到对象」的表，你改了表里的一行，所有此后查这个名字的代码都会看到新的值。典型用途是测试里替换网络调用（`unittest.mock.patch` 就是一个会自动还原的猴子补丁）、给第三方库打热修补。

**`__getattr__`**：对象的属性按固定顺序查找（实例字典、类、父类）。**只有当这些都找不到时**，才会调用类上定义的 `__getattr__(self, name)`，它的返回值就当作该属性的值。

```python
class Lazy:
    def __getattr__(self, name): return f"<dynamic {name}>"
print(Lazy().anything)     # <dynamic anything>
```

心智模型：属性查找的「最后兜底」。用途：代理对象（把未知属性转发给被包装的对象）、按需读取的配置、动态 API 客户端（`client.users.list()` 并没有预先定义 `users`）。

**要记住的一点**：这两个特性都让名字和行为的对应关系在运行时才确定，静态工具读不出来，所以它们的使用要有明确边界。
