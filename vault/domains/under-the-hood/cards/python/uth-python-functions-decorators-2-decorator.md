---
id: uth-python-functions-decorators-2-decorator
node: python.functions-decorators
type: qa
step: 2
---
## Q
**@cache 到底做了什么**｜Python · CPython 3.14

给递归函数加一行 `@cache` 就能记忆化。这一行背后，名字 `fib` 变成了什么？

## A
**背景。** 想给一批函数都加上「记住结果」或「计时」的功能，又不想改每个函数体。函数是对象，所以可以拿一个新函数，把旧函数包起来。

**结构。** `@deco` 写在 `def` 上，等价于定义完函数后执行 `f = deco(f)`：装饰器就是「收一个函数、返回一个函数」的函数，名字 `f` 从此指向返回的新函数。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="10" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">装饰前  def fib 之后</text>
<rect x="10" y="28" width="40" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="30" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">fib</text>
<line x1="50" y1="40" x2="118" y2="40" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,40.0 112.0,43.0 112.0,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="26" width="110" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="175" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">fib 原函数</text>
<line x1="10" y1="76" x2="330" y2="76" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">@cache 之后  fib = cache(fib)</text>
<rect x="10" y="112" width="40" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="30" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">fib</text>
<line x1="50" y1="124" x2="78" y2="124" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="78.0,124.0 72.0,127.0 72.0,121.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="80" y="110" width="100" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="130" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">wrapper</text>
<line x1="180" y1="124" x2="218" y2="124" stroke-width="1.2" stroke="currentColor"/>
<polygon points="218.0,124.0 212.0,127.0 212.0,121.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="220" y="110" width="100" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="270" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">fib 原函数</text>
<text x="200" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">闭包记住</text>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">递归里写的 fib(n - 1)</text>
<text x="170" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">现在查到的是 wrapper</text>
</svg>
```

**细节。**

- 新函数（常叫 `wrapper`）用闭包记住原函数，调用时先做额外的事，再调用原函数。
- `functools.cache` 的函数体只有一行：`lru_cache(maxsize=None)(user_function)`。
- 装饰只发生在 `def` 执行的那一刻，只一次，不是每次调用。
- 多个装饰器从下往上套：`@a @b def f` 等价于 `f = a(b(f))`。

**为什么。** 把缓存、计时这类通用功能和业务代码分开；代价是每次调用多过一层 wrapper。

**坑。** 递归函数装饰之后，函数体里的 `fib(n - 1)` 查到的是装饰后的名字，所以递归调用也走缓存。

**例题：** LC 10 正则表达式匹配

给字符串 `s` 和模式 `p`，实现支持 `.`（任意单字符）和 `*`（前一个字符重复零次或多次）的匹配，要求覆盖整个 `s`。例：`s = "aab"`，`p = "c*a*b"` 得 `true`。

```python
from functools import cache


def is_match(s: str, p: str) -> bool:
    @cache
    def match(i: int, j: int) -> bool:      # s[i:] 能否被 p[j:] 整个匹配
        if j == len(p):
            return i == len(s)
        first = i < len(s) and p[j] in (s[i], '.')   # 当前字符能否匹配 p[j]
        if j + 1 < len(p) and p[j + 1] == '*':
            # 星号两条路：匹配零次（跳过 "x*"），或匹配一次后留在原位继续
            return match(i, j + 2) or (first and match(i + 1, j))
        return first and match(i + 1, j + 1)

    return match(0, 0)
```
