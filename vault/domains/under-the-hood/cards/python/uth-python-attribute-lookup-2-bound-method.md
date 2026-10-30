---
id: uth-python-attribute-lookup-2-bound-method
node: python.attribute-lookup
type: qa
step: 2
---
## Q
**obj.method 为什么每次都是新对象**｜Python · CPython 3.14

`d.bark` 和 `Dog.bark` 有什么不同？`d.bark is d.bark` 为什么是 `False`？

## A
**背景。** 调用 `d.bark()` 时，函数得知道 `self` 是谁。可类里存的只是一个普通函数，它不知道自己被哪个实例取走。所以必须在「取属性」的那一刻，把实例和函数绑到一起。

**结构。** 函数对象实现了 `__get__`（定义了 `__get__` 的对象叫描述符，放在类里时，取属性会调用它）。通过实例取时，`__get__` 返回一个绑定方法对象，里面存着 `__self__`（实例）和 `__func__`（原函数）；调用它就是 `func(self, *args)`。通过类取，则直接得到原函数。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 195">
<rect x="10" y="56" width="62" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41" y="73" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d.bark</text>
<line x1="72" y1="69" x2="100" y2="69" stroke-width="1.2" stroke="currentColor"/>
<polygon points="100.0,69.0 94.0,72.0 94.0,66.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="102" y="36" width="112" height="70" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="158" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">绑定方法</text>
<text x="112" y="74" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">__self__</text>
<text x="112" y="94" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">__func__</text>
<rect x="260" y="56" width="64" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="292" y="73" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例 d</text>
<line x1="214" y1="70" x2="258" y2="68" stroke-width="1.2" stroke="currentColor"/>
<polygon points="258.0,68.0 252.1,71.3 251.9,65.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="260" y="92" width="64" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="292" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">bark 函数</text>
<line x1="214" y1="90" x2="258" y2="102" stroke-width="1.2" stroke="currentColor"/>
<polygon points="258.0,102.0 251.4,103.3 253.0,97.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="158" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次取都新建</text>
<text x="170" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Dog.bark 取到原函数 不绑定</text>
<text x="170" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d.bark() 就是 bark(d)</text>
</svg>
```

**细节。**

- CPython 里是 `func_descr_get` 调 `PyMethod_New`，每次取都新建一个绑定方法对象，所以 `d.bark is d.bark` 为 `False`。
- `d.bark()` 这种直接调用，字节码里的 `LOAD_ATTR` 方法版会跳过创建绑定方法，直接把函数和 `self` 一起压栈。
- `self` 只是第一个位置参数的惯用名，不是关键字。

**坑。** `cb = d.bark` 存下来的绑定方法一直引用着 `d`，`d` 不会被回收。

**对应 LeetCode：** 无直接对应的题
