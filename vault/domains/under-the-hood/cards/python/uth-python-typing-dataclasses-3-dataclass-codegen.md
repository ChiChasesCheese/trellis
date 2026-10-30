---
id: uth-python-typing-dataclasses-3-dataclass-codegen
node: python.typing-dataclasses
type: qa
step: 3
---
## Q
**dataclass 怎样凭空生成 __init__**｜Python · CPython 3.14

只写了两行字段，`@dataclass` 为什么就有了 `__init__`、`__repr__`、`__eq__`？它是一种新的对象模型吗？

## A
**背景。** 只存数据的类，每个都要手写 `__init__`（把参数逐个赋给 `self`）、`__repr__`（打印出来看得懂）、`__eq__`（逐字段比较）。样板代码又长又容易漏字段。

**结构。** `@dataclass` 是类装饰器（接收一个类、返回改好的类的函数）：读类的 `__annotations__` 得到字段名单，拼出方法的源码文本，用 `exec`（运行一段源码文本）编译成函数，挂回类上。生成的就是普通函数，不是新的对象模型。

```python
@dataclass
class P:
    x: int
    y: int = 0
# P(1) -> P(x=1, y=0)
```

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 152">
<rect x="8" y="20" width="92" height="74" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="54" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读字段名单</text>
<text x="54" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x: int</text>
<text x="54" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">y: int = 0</text>
<rect x="124" y="20" width="92" height="74" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拼成源码文本</text>
<text x="170" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">def __init__(</text>
<text x="170" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">self, x, y=0):</text>
<rect x="240" y="20" width="92" height="74" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="286" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">exec 编译</text>
<text x="286" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">挂到类上</text>
<text x="286" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">P.__init__</text>
<line x1="100" y1="57" x2="118.0" y2="57.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="124,57 118.0,60.0 118.0,54.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="216" y1="57" x2="234.0" y2="57.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="240,57 234.0,60.0 234.0,54.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">生成的是普通函数 之后和手写的一样</text>
</svg>
```

**细节。**

- 拼出的 `__init__` 大致是 `def __init__(self, x, y=0): self.x = x; self.y = y`。
- 生成的 `__eq__` 先要求两边类相同，再逐字段比较，否则返回 `NotImplemented`：`P(1) == (1, 0)` 是 `False`。
- 只有带注解的名字才算字段：没有注解的 `z = 1` 只是普通类属性。

**为什么。** 类创建时一次性生成，之后调用的就是普通函数，和手写的没有区别。

**对应 LeetCode：** 无直接对应的题
