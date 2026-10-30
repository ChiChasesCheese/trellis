---
id: uth-python-imports-modules-2-module-object
node: python.imports-modules
type: qa
step: 2
---
## Q
**模块也是对象**｜Python · CPython 3.14

`import json` 之后，`json` 到底是个什么东西？`from json import dumps` 和它有什么区别？

## A
**背景。** 模块要能共享函数和变量，就得有个地方放这些名字。

**结构。** 模块就是一个 `types.ModuleType` 对象，它的全局变量存在自己的 `__dict__` 里。`import json` 只是把当前文件里的名字 `json` 绑到 `sys.modules["json"]` 这个对象上；`from json import dumps` 则是取 `json.dumps`，把函数本身绑到新名字 `dumps` 上。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 172">
<text x="53" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a.py 里的名字</text>
<rect x="8" y="26" width="90" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="53" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">json</text>
<rect x="8" y="78" width="90" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="53" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dumps</text>
<rect x="170" y="20" width="162" height="112" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="180" y="38" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">module json</text>
<text x="180" y="54" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">__dict__</text>
<rect x="182" y="62" width="138" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="251" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dumps = 函数</text>
<rect x="182" y="94" width="138" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="251" y="111" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">loads = 函数</text>
<line x1="98" y1="39" x2="164.0" y2="39.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,39 164.0,42.0 164.0,36.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="98" y1="91" x2="176.1" y2="77.1" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="182,76 176.6,80.0 175.6,74.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">from json import dumps 绑的是函数本身</text>
</svg>
```

**细节。**

- 想要全局共享的单例，直接用模块级变量：所有 `import` 它的人拿到的是同一个模块对象。
- `del sys.modules["json"]` 之后再 `import`，得到的是新对象，手里的旧引用和它不再相同；`importlib.reload` 则在原对象上把代码重跑一遍。

**坑。** `from` 复制的是名字绑定：之后别处重新赋值 `cfg.level`，你手里的 `level` 不会变。

```python
from cfg import level      # cfg.py 里 level = 1
import cfg
cfg.level = 2
print(level, cfg.level)    # 1 2
```

**对应 LeetCode：** 无直接对应的题
