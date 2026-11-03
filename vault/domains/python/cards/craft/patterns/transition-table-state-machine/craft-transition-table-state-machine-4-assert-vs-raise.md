---
id: craft-transition-table-state-machine-4-assert-vs-raise
node: craft.patterns.transition-table-state-machine
type: qa
step: 4
---
## Q
**转移表状态机 · 转移不合法时用 assert 还是抛领域异常**｜模式

熔断器的内部 `_move` 用 `assert new in _TRANSITIONS[self._state]` 守住转移表，而航班、叫车题对非法转移抛领域异常。这两种选择差别在哪？为什么不全用 assert？

## A
**要点。** 看非法转移是谁造成的。调用方的输入造成（用户对已发货订单点取消）：这是正常的运行期错误，必须抛领域异常并一直保留。只有代码自己的内部调用造成（熔断器自己决定从哪个状态去哪个状态），非法就是程序员的 bug，才适合 assert。

```python
def move(allowed, new):
    assert new in allowed, f"非法转换 -> {new}"
    print("转换到", new)

move({"OPEN"}, "CLOSED")
```

同一个文件，普通运行与 `python -O` 运行对比：

```
AssertionError: 非法转换 -> CLOSED
转换到 CLOSED
```

**易错。** `python -O`（或 `PYTHONOPTIMIZE`）会整个删掉 assert 语句：保护还在代码里，运行时却没了，非法转移被悄悄放行，对外 API 绝不能用它守业务规则。

**代价。** 抛领域异常要多定义一个异常类、多一个分支；换来的是调用方能 `except` 它并给用户可读的错误。

**为什么。** 熔断器的 `_move` 同时做了 `self._gen += 1`：每次转移让所有在途的旧许可作废，这是把转移和代号绑在一个函数里的好处，非法路径一开始就进不来。
