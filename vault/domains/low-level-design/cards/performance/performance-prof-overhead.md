---
id: performance-prof-overhead
node: performance.profiling
type: qa
step: 2
---
## Q
`cProfile` 告诉你生成器表达式是热点，改完后怎么确认真的变快了？为什么不能直接拿剖析下的耗时当作“程序运行多快”？

## A
**剖析器会拖慢程序、扭曲占比；用它定位，用 `timeit` 验证**

- **`cProfile` 是确定性剖析器**：每次函数调用和返回都记一笔，调用次数越多，开销越大；
- **小而密集的调用被夸大**：下面的例子里没剖析 3.8 ms，开着剖析 22.0 ms，慢了约 6 倍，几乎都是记账成本；
- **所以别信剖析下的绝对耗时**：它给出的是排序和相对比例，大头是谁；
- **改完用 `timeit` 重量**：不开任何工具，同一份输入、取最小值，和改之前对比；
- **同时看剖析的调用次数**：剖析器计的次数是准的，次数从 17 万降到 2 万，就说明这条路径缩短了。

实测（3.11，本机，2 万行数据，整条流程“规范化 + 求和”，每次调用耗时）：

| 版本 | 耗时 |
|---|---|
| 原版，不开剖析 | 3.8 ms |
| 原版，开着 `cProfile` | 22.0 ms（约 6 倍） |
| 改成 `sum(w.encode("ascii"))`，不开剖析 | 1.5 ms |

```python
import timeit

def normalize(s): return s.strip().lower()
def score(ws): return sum(sum(ord(c) for c in w) for w in ws)
def score_fast(ws): return sum(sum(w.encode("ascii")) for w in ws)   # 只适用于纯 ASCII

rows = [f"  Row{i} " for i in range(20000)]
def run(sc): return sc([normalize(r) for r in rows])               # 整条流程
assert run(score) == run(score_fast)                               # 先确认结果一致
for sc in (score, score_fast):
    print(sc.__name__, round(min(timeit.repeat(lambda: run(sc), number=1, repeat=7)) * 1e3, 2), "ms")
```

<details class="pt"><summary>延伸</summary>

`score_fast` 只在文本是 ASCII 时和原版等价（`encode("ascii")` 遇到别的字符会抛异常）。性能优化缩小了输入范围，要写进注释，并用测试守住。

</details>

**知识点：**读懂剖析结果（Reading Profiles）
