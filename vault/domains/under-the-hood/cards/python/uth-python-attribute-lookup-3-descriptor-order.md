---
id: uth-python-attribute-lookup-3-descriptor-order
node: python.attribute-lookup
type: qa
step: 3
---
## Q
**同名的实例属性和类属性，谁赢**｜Python · CPython 3.14

给实例写 `d.bark = ...` 能盖掉类里的方法，却盖不掉 `@property`。取属性时的优先级到底是什么？

## A
**背景。** 实例和类里可能放着同名属性。优先级必须固定，否则同一行代码的结果就没法预料。

**结构。** 取 `d.x` 的步骤如下（CPython 的 `object.__getattribute__`）：先在类和父类里找名字，找到数据描述符就直接用它，否则才看实例字典。数据描述符是定义了 `__set__` 或 `__delete__` 的对象，如 `property`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="10" y="8" width="320" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="20" y="29" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 在类和父类里找这个名字</text>
<line x1="170" y1="40" x2="170" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,56.0 167.0,50.0 173.0,50.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="56" width="320" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="20" y="77" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 找到数据描述符 调它的 __get__</text>
<line x1="170" y1="88" x2="170" y2="104" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,104.0 167.0,98.0 173.0,98.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="104" width="320" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="20" y="125" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3 实例字典里有 返回它</text>
<line x1="170" y1="136" x2="170" y2="152" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,152.0 167.0,146.0 173.0,146.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="152" width="320" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="20" y="173" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">4 非数据描述符调 __get__ 否则返回类属性</text>
<line x1="170" y1="184" x2="170" y2="200" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,200.0 167.0,194.0 173.0,194.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="200" width="320" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="20" y="221" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">5 都没有 AttributeError</text>
</svg>
```

**细节。**

| 类里找到的是 | 实例字典里有同名 | 结果 |
|---|---|---|
| 数据描述符（`property`、slots 成员） | 无所谓 | 调描述符，实例字典被无视 |
| 函数（只有 `__get__` 的非数据描述符） | 有 | 实例的值赢 |
| 普通类属性 | 有 | 实例的值赢 |

**为什么。** 数据描述符要能强制执行 getter 和 setter（比如只读），所以必须压过实例字典；方法则允许单个对象覆盖。

**对应 LeetCode：** 无直接对应的题
