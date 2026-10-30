---
id: uth-python-typing-dataclasses-2-generic-alias
node: python.typing-dataclasses
type: qa
step: 2
---
## Q
**list[int] 和 int | None 是什么对象**｜Python · CPython 3.14

注解里的 `list[int]`、`int | None` 在运行时是真对象吗？拿它们做 `isinstance` 会怎样？

## A
**背景。** 注解里想表达「元素是 int 的列表」。最省事的办法，是让内置的 `list` 直接支持下标语法，不必再另造一套 `typing.List`。

**结构。** `list[int]` 调用的是 `list.__class_getitem__(int)`，得到一个 `types.GenericAlias` 对象（3.9 起），只记录 `__origin__ = list` 和 `__args__ = (int,)`。`int | None` 调用 `type.__or__`（3.10 起），得到一个联合类型对象；3.14 起它的类型就是 `typing.Union`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 152">
<rect x="8" y="22" width="96" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="56" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">list[int]</text>
<line x1="104" y1="37" x2="122.0" y2="37.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,37 122.0,40.0 122.0,34.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="128" y="8" width="204" height="58" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="140" y="26" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">types.GenericAlias</text>
<text x="140" y="44" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">__origin__ = list</text>
<text x="140" y="60" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">__args__ = (int,)</text>
<rect x="8" y="92" width="96" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="56" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">int | None</text>
<line x1="104" y1="107" x2="122.0" y2="107.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,107 122.0,110.0 122.0,104.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="128" y="78" width="204" height="58" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="140" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">typing.Union</text>
<text x="140" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">__args__ =</text>
<text x="140" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">(int, NoneType)</text>
<text x="56" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只是标签</text>
</svg>
```

**细节。**

- 它们只是标签，不检查内容：`list[str]([1, 2, 3])` 照样得到 `[1, 2, 3]`，而且得到的就是普通 `list`。
- `isinstance(x, list[int])` 直接抛 `TypeError`：运行时不知道元素类型，要写 `isinstance(x, list)`；`isinstance(x, int | str)` 可以用。

**坑。** `int | "Foo"`（`Foo` 是字符串形式的前向引用）在运行时会失败，要把整个表达式写成字符串 `"int | Foo"`。

**对应 LeetCode：** 无直接对应的题
