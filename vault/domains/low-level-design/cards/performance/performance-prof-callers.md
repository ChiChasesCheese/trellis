---
id: performance-prof-callers
node: performance.profiling
type: qa
step: 4
---
## Q
剖析结果里排第一的是一个到处被调用的小函数（比如 `<genexpr>` 或字符串处理函数）。光知道它慢不够，怎么知道该改谁、改成什么？剖析报告上的“火焰图”又是怎么读的？

## A
**热点函数要往上看“谁调用了它”，往往改调用方比改它自己更有效**

- **`pstats` 的 `print_callers(名字)`**：列出调用者、每个调用者调用了多少次、花了多少时间；
- **次数比单次耗时更重要时，改调用方**：让它少调用几次（批量、提前过滤、缓存），而不是把单次再抠快一点；
- **火焰图（flame graph）**：横轴宽度是时间占比（不是时间先后），纵轴是调用栈，下面是调用者，上面是被调用者；最宽、顶端是平的那一块就是热点；
- **火焰图来自采样剖析器**：按固定间隔看栈在哪，开销小，对 `py-spy` 这类外部工具不需要改代码，适合线上；`cProfile` 是确定性的，开发时用；
- **改完重新剖析、重新计时**：看调用次数和耗时是否真的降了，而不是只看代码改得漂不漂亮。

```python
import cProfile, pstats

def normalize(s): return s.strip().lower()
def score(words): return sum(sum(ord(c) for c in w) for w in words)
def main(): return score([normalize(f"  Row{i} ") for i in range(20000)])

pr = cProfile.Profile(); pr.enable(); main(); pr.disable()
pstats.Stats(pr).strip_dirs().print_callers("genexpr")
```

本机 3.11 的输出：

```text
Function               was called by...
                           ncalls  tottime  cumtime
demo.py:4(<genexpr>)  <-  168890    0.012    0.016  {built-in method builtins.sum}
```

生成器表达式 16.9 万次调用，全部来自 `sum`；每个单词生成一个生成器、逐字符调用 `ord`，所以要改的是“逐字符”这个写法，而不是 `ord`。

**知识点：**读懂剖析结果（Reading Profiles）
