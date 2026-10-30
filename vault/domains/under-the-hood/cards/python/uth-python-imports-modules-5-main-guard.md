---
id: uth-python-imports-modules-5-main-guard
node: python.imports-modules
type: qa
step: 5
---
## Q
**if __name__ == "__main__" 是什么意思**｜Python · CPython 3.14

同一个文件，直接运行和被 `import` 时，`if __name__ == "__main__":` 下面的代码为什么只有前一种会执行？

## A
**背景。** 一个文件既想当程序直接跑，又想被别人当库 `import`；`import` 时不该顺带把程序启动。文件得知道「现在是谁在执行我」。

**结构。** 每个模块都有 `__name__`：被 `import` 时是模块名（如 `m`）；而入口文件，也就是 `python m.py` 或 `python -m m` 里运行的那个，解释器把它当作名叫 `__main__` 的模块来执行，`__name__` 就是 `"__main__"`。守卫判断的就是「我是入口吗」。

**坑。** 入口文件在 `sys.modules` 里登记的名字是 `__main__`，不是 `m`。如果别的模块又 `import m`，会再加载一遍：同一个文件有了两个模块对象，顶层代码跑两遍。`python m.py` 里再 `import m`，先后打印「run as __main__」「run as m」。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">sys.modules</text>
<rect x="10" y="26" width="110" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="65" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">"__main__"</text>
<rect x="10" y="70" width="110" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="65" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">"m"</text>
<line x1="120" y1="41" x2="162.0" y2="41.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="168,41 162.0,44.0 162.0,38.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="120" y1="85" x2="162.0" y2="85.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="168,85 162.0,88.0 162.0,82.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="168" y="26" width="164" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">m.py 第 1 份 入口</text>
<rect x="168" y="70" width="164" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="250" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">m.py 第 2 份 被 import</text>
<text x="170" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同一个文件 两个模块对象</text>
<text x="170" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">顶层代码跑两次</text>
</svg>
```

**细节。**

- `python -m pkg` 执行的是包里的 `__main__.py`。

**对应 LeetCode：** 无直接对应的题
