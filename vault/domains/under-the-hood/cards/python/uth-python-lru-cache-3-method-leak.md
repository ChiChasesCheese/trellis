---
id: uth-python-lru-cache-3-method-leak
node: python.lru-cache
type: qa
step: 3
---
## Q
**给方法加 lru_cache 为什么会内存泄漏**｜Python · CPython 3.14

在类的方法上用 `@lru_cache(maxsize=None)`，实例 `del` 之后为什么还活着？

## A
**背景。** 缓存要按参数查结果，所以必须把参数留着当 key。方法的第一个参数是 `self`，也是 key 的一部分，缓存就一直握着这个实例。

**结构。** 缓存挂在函数上，不在实例上；缓存的 `dict` 持有 key，也就持有了 `self`，实例的引用计数（有几个地方指着它）不会归零。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<rect x="20" y="40" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">变量 a</text>
<rect x="150" y="40" width="80" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="190" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例</text>
<line x1="76" y1="54" x2="150" y2="54" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="103" y1="44" x2="123" y2="64" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="123" y1="44" x2="103" y2="64" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="113" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">del a</text>
<rect x="100" y="120" width="190" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="195" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缓存 dict</text>
<rect x="120" y="146" width="150" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="195" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">key = (self, 1)</text>
<line x1="190" y1="120" x2="190" y2="70" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190.0,70.0 193.0,76.0 187.0,76.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="202" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">key 里握着 self</text>
<text x="250" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">仍活着</text>
</svg>
```

**细节。**

- 实测：调用 `a.m(1)` 后 `del a`，再 `gc.collect()`，弱引用（不占引用计数的指针）仍然指向存活的实例。
- 有大小上限时，实例要等被淘汰出缓存才会释放。

**为什么。** 缓存的寿命等同函数本身，key 必须强引用才能比较。

**坑。** 要按实例缓存，就在 `__init__` 里给每个实例单独包一个缓存函数。

**对应 LeetCode：** 无直接对应的题
