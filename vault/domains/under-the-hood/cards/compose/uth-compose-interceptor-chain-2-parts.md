---
id: uth-compose-interceptor-chain-2-parts
node: compose.interceptor-chain
type: qa
step: 2
---
## Q
**一个列表加一个游标**｜Spring AOP · 7.0

拦截器链在 Spring AOP 里由哪几个结构组成？`proceed()` 怎样找到下一环？

## A
**结构。** 有序列表 `interceptorsAndDynamicMethodMatchers` 存各环；每次调用新建一个 `ReflectiveMethodInvocation`，里面有游标 `currentInterceptorIndex`（初值 -1）和目标方法。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="46" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">列表 chain</text>
<rect x="4" y="52" width="248" height="44" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="10" y="58" width="68" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拦截器 0</text>
<rect x="94" y="58" width="68" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="128.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拦截器 1</text>
<rect x="178" y="58" width="68" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拦截器 2</text>
<rect x="262" y="58" width="68" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="296.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">目标方法</text>
<line x1="78" y1="74" x2="94" y2="74" stroke-width="1.2" stroke="currentColor"/>
<polygon points="94.0,74.0 89.0,76.5 89.0,71.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="162" y1="74" x2="178" y2="74" stroke-width="1.2" stroke="currentColor"/>
<polygon points="178.0,74.0 173.0,76.5 173.0,71.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="246" y1="74" x2="262" y2="74" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262.0,74.0 257.0,76.5 257.0,71.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="128.0" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">index = 1</text>
<line x1="128.0" y1="22" x2="128.0" y2="56" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128.0,56.0 125.5,51.0 130.5,51.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="14" y="122" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">proceed(): index 加一 调用 chain[index]</text>
<text x="14" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">游标到了最后一环 再 proceed(): 调目标方法</text>
<text x="14" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">某一环不调用 proceed(): 后面的全被拦下</text>
<text x="14" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">游标属于这一次调用 不属于列表</text>
</svg>
```

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| 建链（每个方法一次） | 把匹配的拦截器按序收进列表 | O(n) |
| `proceed()` | 游标加一，取列表里下一环并调用 | O(1) |
| 游标到了最后一环 | 调用目标方法 | O(1) |
| 拦下 | 某一环不调用 `proceed()` | O(1) |

**细节。** 一次调用把每一环各走一次，总共 O(n)。

**例题：** LC 1472 设计浏览器历史记录

实现 `BrowserHistory`：用主页初始化；`visit(url)` 访问新页面并清空所有能前进到的记录；`back(steps)` 后退最多 `steps` 步，越界就退到最前一页；`forward(steps)` 前进最多 `steps` 步，越界就进到最后一页；后两者返回落点 URL。同样是“列表 + 游标”，只是游标能前后移动。

```python
class BrowserHistory:
    def __init__(self, homepage: str) -> None:
        self.history: list[str] = [homepage]
        self.cursor = 0

    def visit(self, url: str) -> None:
        del self.history[self.cursor + 1:]
        self.history.append(url)
        self.cursor += 1

    def back(self, steps: int) -> str:
        self.cursor = max(0, self.cursor - steps)
        return self.history[self.cursor]

    def forward(self, steps: int) -> str:
        self.cursor = min(len(self.history) - 1, self.cursor + steps)
        return self.history[self.cursor]
```
