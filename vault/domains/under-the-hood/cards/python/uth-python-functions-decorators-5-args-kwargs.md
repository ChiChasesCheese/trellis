---
id: uth-python-functions-decorators-5-args-kwargs
node: python.functions-decorators
type: qa
step: 5
---
## Q
**函数参数里的星号：收下与拆开**｜Python · CPython 3.14

定义函数时的 `*args`、调用时的 `f(*seq)` 各做什么？为什么 `zip(*matrix)` 能转置矩阵？

## A
**背景。** 有的函数参数个数不固定，比如 `print(1, 2, 3)`。定义时要能「收下多出来的」，调用时要能「把一个列表拆开传」。

**结构。** 定义时：`*args` 把多出来的位置参数收成一个元组，`**kwargs` 把多出来的关键字参数收成一个字典。调用时：`f(*seq)` 把序列拆成一个个位置参数，`f(**d)` 把字典拆成关键字参数。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="10" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">matrix</text>
<rect x="10" y="28" width="70" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="45" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[1, 2]</text>
<line x1="80" y1="40" x2="128" y2="70" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.0,70.0 121.3,69.4 124.5,64.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="58" width="70" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="45" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[3, 4]</text>
<line x1="80" y1="70" x2="128" y2="70" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.0,70.0 122.0,73.0 122.0,67.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="88" width="70" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="45" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[5, 6]</text>
<line x1="80" y1="100" x2="128" y2="70" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.0,70.0 124.5,75.7 121.3,70.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="130" y="50" width="90" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="175" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">zip(r0, r1, r2)</text>
<text x="104" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">*matrix 拆开</text>
<line x1="220" y1="62" x2="250" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,52.0 245.3,56.7 243.4,51.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="220" y1="78" x2="250" y2="88" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,88.0 243.4,88.9 245.3,83.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="252" y="38" width="78" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="291" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">(1, 3, 5)</text>
<rect x="252" y="76" width="78" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="291" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">(2, 4, 6)</text>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f(*seq) 拆成一个个位置参数</text>
<text x="170" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">def f(*args) 把多出的位置参数收成元组</text>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">def f(**kw) 把多出的关键字参数收成字典</text>
</svg>
```

**细节。**

- `zip(*matrix)` 就是 `zip(row0, row1, row2, ...)`，`zip` 再把每行的第 j 个凑成一列，于是转置。
- 填参数的顺序：先按位置填，再按名字填，剩下的用默认值；多出来的才进 `*`、`**`。
- 同一个参数被填了两次，报 `TypeError`。
- `*` 之后的参数只能用名字传，`/` 之前的参数只能按位置传。

**为什么。** 参数个数可变，才能写出 `print`、`zip` 这样的通用函数。

**例题：** LC 14 最长公共前缀

给字符串数组 `strs`，求所有字符串的最长公共前缀，没有就返回 `""`。例：`["flower","flow","flight"]` 得 `"fl"`。

```python
def longest_common_prefix(strs: list[str]) -> str:
    size = 0
    for column in zip(*strs):                    # 按列扫：第 j 列是所有字符串的第 j 个字符；zip 在最短串处自动停
        if len(set(column)) != 1:                # 这一列有不同字符：前缀到此为止
            break
        size += 1
    return strs[0][:size]
```
