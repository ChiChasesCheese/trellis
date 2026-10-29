---
id: uth-compose-interceptor-chain-3-onion-code
node: compose.interceptor-chain
type: qa
step: 3
---
## Q
**不变量与核心代码：洋葱模型**｜Spring AOP · 7.0

拦截器链要守住哪些不变量？为什么 `proceed()` 之后的代码是倒着执行的？用不到 30 行的 Python 写出来。

## A
**不变量。**

- 游标只增不减，每个拦截器被进入一次，进入顺序就是列表顺序
- `proceed()` 返回之后才执行的收尾，顺序和进入相反：它们排在调用栈里，先进后出，叫洋葱模型
- 一次调用一个调用对象，游标是它私有的；列表建好后只读，可以被很多次调用共享

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="170" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">进入: 前处理 先 A 后 B</text>
<rect x="24" y="34" width="70" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="59.0" y="60.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拦截器 A</text>
<rect x="135" y="34" width="70" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="60.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拦截器 B</text>
<rect x="246" y="34" width="70" height="44" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="281.0" y="60.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">目标方法</text>
<line x1="94" y1="48" x2="135" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="135.0,48.0 130.0,50.5 130.0,45.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="135" y1="64" x2="94" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="94.0,64.0 99.0,61.5 99.0,66.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="205" y1="48" x2="246" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="246.0,48.0 241.0,50.5 241.0,45.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="246" y1="64" x2="205" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="205.0,64.0 210.0,61.5 210.0,66.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回: 后处理 先 B 后 A</text>
<text x="170" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">A 前 B 前 目标 B 后 A 后</text>
<text x="170" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先进后出 像剥洋葱 一层层返回</text>
</svg>
```

**核心代码。**

```python
from collections.abc import Callable

Interceptor = Callable[["Invocation"], object]


class Invocation:
    def __init__(self, chain: list[Interceptor], target: Callable[[], object]) -> None:
        self.chain = chain                              # 有序列表：建好后只读，可以被很多次调用共享
        self.target = target                            # 链尾真正要执行的方法
        self.index = -1                                 # 游标：已经进入到第几环；属于这一次调用

    def proceed(self) -> object:
        if self.index == len(self.chain) - 1:           # 所有拦截器都进入过了：调用目标方法
            return self.target()
        self.index += 1                                 # 游标只增不减
        return self.chain[self.index](self)             # 这一环自己决定调不调 proceed()


def tag(name: str, trace: list[str]) -> Interceptor:
    def interceptor(inv: Invocation) -> object:
        trace.append(f"{name} 前")                      # proceed() 之前：前处理，按列表顺序
        result = inv.proceed()                          # 不调用这一句，就是拦截：后面的环和目标都不执行
        trace.append(f"{name} 后")                      # proceed() 之后：后处理，顺序和进入相反
        return result
    return interceptor


trace: list[str] = []
Invocation([tag("A", trace), tag("B", trace)], lambda: trace.append("目标")).proceed()
# trace == ["A 前", "B 前", "目标", "B 后", "A 后"]
```

**对应 LeetCode：** 无直接对应的题
