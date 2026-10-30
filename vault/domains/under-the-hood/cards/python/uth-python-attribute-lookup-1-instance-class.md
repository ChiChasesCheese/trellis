---
id: uth-python-attribute-lookup-1-instance-class
node: python.attribute-lookup
type: qa
step: 1
---
## Q
**obj.x 先去哪找**｜Python · CPython 3.14

`d.name` 和 `d.bark()` 都写成 `d.xxx`，Python 怎么知道前者在实例里、后者在类里？

## A
**背景。** 每个对象的数据（名字、血量）各不相同，必须各存各的；方法对同一个类的所有对象都一样，没必要每个对象抄一份。所以数据放在实例里，方法放在类里。取属性时就得规定：先看哪里，找不到再看哪里。

**结构。** 实例有自己的属性表（`__dict__`），类有一张表（里面放方法），查不到还会继续往父类走。常见情形下，`d.x` 是先查实例，再沿着类、父类逐个查。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<rect x="10" y="18" width="200" height="36" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="20" y="33" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">d.__dict__</text>
<text x="20" y="48" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">name: "Rex"</text>
<text x="222" y="40" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d.name 在这里</text>
<line x1="110" y1="54" x2="110" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="110.0,84.0 107.0,78.0 113.0,78.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="122" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有 再往上找</text>
<rect x="10" y="84" width="200" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="20" y="99" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Dog.__dict__</text>
<text x="20" y="114" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">bark: 函数</text>
<text x="222" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d.bark 在这里</text>
<line x1="110" y1="120" x2="110" y2="150" stroke-width="1.2" stroke="currentColor"/>
<polygon points="110.0,150.0 107.0,144.0 113.0,144.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="122" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有 再往上找</text>
<rect x="10" y="150" width="200" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="20" y="165" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Animal.__dict__</text>
<text x="20" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">eat: 函数</text>
<text x="222" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d.eat 在这里</text>
<text x="170" y="210" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数据在实例里 方法只存一份在类里</text>
</svg>
```

**细节。**

- 方法只存一份在类里，一万个实例共用；改类上的方法，已有的实例立刻生效。
- `d.x = 1` 的写入总是落在实例上，不会改类：`inst.x = inst.x + 1` 读到类里的 3，写出实例上的 4，类里仍是 3。
- 3.11 起实例的 `__dict__` 延迟创建：没人读它时，属性值存在更紧凑的内部结构里，对外行为不变。
- 哪里都没有：`AttributeError`。

**坑。** 类里若放着「描述符」这种特殊对象，查找的优先级会变，比如 `property` 就不会被实例属性盖住。

**对应 LeetCode：** 无直接对应的题
