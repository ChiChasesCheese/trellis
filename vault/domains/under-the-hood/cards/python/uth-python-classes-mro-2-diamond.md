---
id: uth-python-classes-mro-2-diamond
node: python.classes-mro
type: qa
step: 2
---
## Q
**多继承：先查哪个父类**｜Python · CPython 3.14

`D(B, C)` 的两个父类 `B`、`C` 都继承 `A`，且 `C` 重写了 `A.f`。`D().f()` 调到谁？Python 怎样事先定下查找顺序？

## A
**背景。** 单继承只有一条链，沿父类往上找就行。多继承会出现「菱形」：`D` 有两个父类，它们又共用同一个祖先 `A`。朴素做法是深度优先、从左到右，顺序成了 `D → B → A → C`：先碰到最老的 `A.f`，`C` 里更新的版本反而被盖住。

**结构。** Python 在建类时就给每个类算好一个固定的查找顺序，叫方法解析顺序（MRO，method resolution order），存在 `__mro__` 里。查方法就是按这个顺序逐个看每个类的字典，第一个有这个名字的就用。菱形的结果是 `D → B → C → A → object`：祖先一定排在它的所有子类后面。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="135" y="15" width="70" height="30" rx="3"/>
<rect x="45" y="85" width="70" height="30" rx="3"/>
<rect x="135" y="155" width="70" height="30" rx="3"/>
<line x1="75" y1="85" x2="150" y2="47"/>
<line x1="265" y1="85" x2="190" y2="47"/>
<line x1="150" y1="155" x2="85" y2="117"/>
<line x1="190" y1="155" x2="255" y2="117"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="225" y="85" width="70" height="30" rx="3"/>
</g>
<g style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)">
<circle cx="125" cy="170" r="9"/>
<circle cx="35" cy="100" r="9"/>
<circle cx="215" cy="100" r="9"/>
<circle cx="125" cy="30" r="9"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="150.0,47.0 146.0,52.4 143.3,47.0"/>
<polygon points="190.0,47.0 196.7,47.0 194.0,52.4"/>
<polygon points="85.0,117.0 91.7,117.4 88.7,122.6"/>
<polygon points="255.0,117.0 251.3,122.6 248.3,117.4"/>
</g>
<g fill="currentColor">
<text x="170" y="34">A: f</text>
<text x="80" y="104">B</text>
<text x="260" y="104">C: f</text>
<text x="170" y="174">D(B, C)</text>
<text x="125" y="174">1</text>
<text x="35" y="104">2</text>
<text x="215" y="104">3</text>
<text x="125" y="34">4</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="170" y="205">按 1 2 3 4 找 f, 先命中 C</text>
</g>
</g>
</svg>
```

```python
class A:
    def f(self): return "A"
class B(A): pass
class C(A):
    def f(self): return "C"
class D(B, C): pass     # D().f() 得到 'C'
```

**细节。**

- 实测 `D.__mro__` 是 `(D, B, C, A, object)`。
- 单继承时顺序就是「自己 + 父类的 MRO」，直接拼接。
- 每次取属性并不真的逐类扫描：CPython 有一张类型属性缓存，共 4096 项，按（类的版本号，属性名）索引。

**为什么。** 建类时一次算好，之后每次查找只是顺序扫描，结果可预测；代价是父类的书写顺序会改变结果。

**对应 LeetCode：** 无直接对应的题
