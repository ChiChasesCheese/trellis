---
id: uth-python-classes-mro-1-class-is-object
node: python.classes-mro
type: qa
step: 1
---
## Q
**类也是对象：class 语句做了什么**｜Python · CPython 3.14

`class Dog:` 执行完之后，`Dog` 是什么？`type(Dog)` 又是什么？

## A
**背景。** 在 C++ 或 Java 里，类只是写在源码里的「图纸」，运行时只有按图纸造出来的对象。Python 没有这个区别：类本身也是一个活的对象，运行时才造出来，能放进变量、当参数传、被修改。那是谁造出类的？是一个专门造类的类，名字叫 `type`。

**结构。** 执行 `class Dog(Animal): ...` 时，Python 先把类体当一段代码跑一遍，所有名字收进一个字典，再调用 `type("Dog", (Animal,), 那个字典)`，得到类对象 `Dog`。于是有三层：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="10" y="40" width="90" height="32" rx="3"/>
<path d="M 305 72 L 305 100 L 265 100 L 265 76"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="125" y="40" width="90" height="32" rx="3"/>
<rect x="240" y="40" width="90" height="32" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="100" y1="56" x2="125" y2="56"/>
<line x1="215" y1="56" x2="240" y2="56"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="265,72 262,79 268,79"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="125.0,56.0 119.0,59.0 119.0,53.0"/>
<polygon points="240.0,56.0 234.0,59.0 234.0,53.0"/>
</g>
<g fill="currentColor">
<text x="55" y="60">d = Dog()</text>
<text x="170" y="60">Dog</text>
<text x="285" y="60">type</text>
<text x="170" y="150">实例 → 类 → type: 每一层都是对象</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="285" y="118">type(type)</text>
<text x="285" y="134">还是 type</text>
<text x="170" y="100">方法 / 类变量</text>
<text x="170" y="115">存在类的字典里</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="112" y="34" font-size="11">type(d)</text>
<text x="228" y="34" font-size="11">type(Dog)</text>
</g>
</g>
</svg>
```

**细节。**

- 实测 `type(d)` 是 `Dog`，`type(Dog)` 是 `type`，`type(type)` 还是 `type`。
- 类对象里存着方法和类变量的字典，还有查找顺序 `__mro__`。`d.bark()` 就是去 `type(d)` 的字典里找 `bark`。
- `int`、`list` 这些内置类型也是 `type` 的实例。

**为什么。** 类是对象，运行时就能造类：`type("T", (A,), {"g": lambda self: 1})` 一行得到新类。枚举 `Enum` 和抽象基类 `ABC` 就是靠换掉造类者实现的（它们的类型分别是 `EnumType`、`ABCMeta`）。

**对应 LeetCode：** 无直接对应的题
