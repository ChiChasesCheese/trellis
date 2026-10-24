---
id: pl-meta-dynamic-pitfall-masked-errors
node: metaprogramming.dynamic-features
type: qa
step: 10
---
## Q
`__getattr__` 与猴子补丁在生产中最常见的两种事故是什么？真实表现是什么？

## A
**事故一：`__getattr__` 吞掉了真正的 bug。** 兜底函数对任何名字都返回值，于是拼错的属性名不再报错。更隐蔽的是：`property` 内部抛出的 `AttributeError`（比如里面的变量名拼错）会被 Python 当作「这个属性不存在」，转而调用 `__getattr__`。

```python
class C:
    @property
    def val(s): return s._vv        # typo inside the property
    def __getattr__(s, name): return f"<dynamic {name}>"
print(C().val)    # <dynamic _vv>
```

真实输出：`<dynamic _vv>`。没有异常，没有栈，一个拼写错误变成了一个看起来正常的字符串，可能流到数据库里。

**防线**：`__getattr__` 里只处理白名单；其余 `raise AttributeError(name)`；单元测试断言不存在的属性会抛异常。

**事故二：猴子补丁泄漏。** 补丁是进程级全局状态，如果测试里忘了还原，后续测试（甚至其他线程）看到的就是被替换的版本。表现是：单个测试通过，整套测试按特定顺序执行时失败，换个顺序又好了，难以复现。上面例子里 `json.dumps = lambda ...` 在恢复之前，所有调用方都得到字符串 `patched`。

**防线**：补丁一律通过会自动还原的工具（`mock.patch` 的上下文管理器或装饰器、pytest `monkeypatch`）；补丁对象写在**使用方**的命名空间（`patch("myapp.client.requests.get")`），而不是库自己的；并行测试时避免共享可变的全局补丁。

共同原则：动态特性把错误从「立即爆炸」变成「悄悄传播」，所以要在边界处主动加断言，把它们变回显式。
