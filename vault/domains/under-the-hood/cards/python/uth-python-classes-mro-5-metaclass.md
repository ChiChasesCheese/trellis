---
id: uth-python-classes-mro-5-metaclass
node: python.classes-mro
type: qa
step: 5
---
## Q
**元类：什么时候才需要**｜Python · CPython 3.14

想在「某个类被创建」的那一刻登记、检查或改写点什么，必须写元类吗？

## A
**背景。** 既然类是 `type` 造出来的，想干预「造类」这件事，就要换掉造类的那个东西，它叫元类（metaclass，类的类）。但多数时候你只想在子类出现时记一笔或检查一下，用不着这么重。

**结构。** `class C(B, metaclass=Meta): ...` 的最后一步是调用 `Meta("C", (B,), 命名空间字典)`。不写 `metaclass` 时，取所有父类的元类里「最派生」的那个，默认是 `type`；父类的元类互不相关就 `TypeError`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="30" y="10" width="280" height="30" rx="3"/>
<rect x="30" y="62" width="280" height="30" rx="3"/>
<line x1="170" y1="40" x2="170" y2="62"/>
<rect x="30" y="166" width="280" height="30" rx="3"/>
<line x1="170" y1="144" x2="170" y2="166"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="30" y="114" width="280" height="30" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="170" y1="92" x2="170" y2="114"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="170.0,62.0 167.0,56.0 173.0,56.0"/>
<polygon points="170.0,166.0 167.0,160.0 173.0,160.0"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="170.0,114.0 167.0,108.0 173.0,108.0"/>
</g>
<g fill="currentColor">
<text x="170" y="29">class C(B, metaclass=Meta): ...</text>
<text x="170" y="81">1 跑类体, 名字收进一个字典</text>
<text x="170" y="133">2 调用 Meta('C', (B,), 字典)</text>
<text x="170" y="185">3 回调 __init_subclass__ 等钩子</text>
</g>
</g>
</svg>
```

**细节。**

- 真正的元类：`enum.Enum` 的元类是 `EnumType`，`abc.ABC` 的是 `ABCMeta`（实测）。
- Python 3.6 起有更轻的钩子：父类里定义 `__init_subclass__`，每建出一个子类就被调用一次：

```python
class Plugin:
    registry = []
    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        Plugin.registry.append(cls)
```

**为什么。** 元类威力最大，却最难组合：一个类只能有一个元类，两个库各带一个互不相关的元类就冲突。能用 `__init_subclass__`、类装饰器、`__set_name__` 解决的，就别用元类。

**对应 LeetCode：** 无直接对应的题
