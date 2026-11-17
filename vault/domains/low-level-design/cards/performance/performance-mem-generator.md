---
id: performance-mem-generator
node: performance.memory
type: qa
step: 1
---
## Q
`sum([x * x for x in range(N)])` 和 `sum(x * x for x in range(N))` 结果一样。内存上差在哪里？什么情况下生成器（generator）反而不合适？

## A
**生成器一次只产生一个元素，内存和 N 无关；列表要把全部放进内存**

- **列表推导式先建完整列表**：一百万个元素，每个整数对象加指针，峰值内存几十 MB；
- **生成器表达式逐个产出、逐个消费**：峰值只有当前一个元素，几百字节；
- **时间几乎一样**：省的是内存，不是 CPU；这里生成器甚至略慢，因为每个元素多一次暂停和恢复；
- **只能遍历一次**：消费完就空了；要多次遍历、要 `len()`、要按下标取、要排序，就该用列表；
- **接口也适用**：函数返回生成器，调用方可以边读边处理，不必等全部算完（见分页那张卡）。

实测（3.11，本机，`tracemalloc` 峰值，N = 1,000,000）：

| 写法 | 峰值内存 | 耗时（不开 tracemalloc） |
|---|---|---|
| `sum([x*x for x in range(N)])` | 40.4 MB | 15.8 ms |
| `sum(x*x for x in range(N))` | 0.0005 MB | 16.9 ms |

```python
import tracemalloc

def peak(f):
    tracemalloc.start(); f()
    _, p = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return p / 1e6

N = 1_000_000
print(round(peak(lambda: sum([x * x for x in range(N)])), 1), "MB")   # 约 40
print(round(peak(lambda: sum(x * x for x in range(N))), 4), "MB")     # 约 0.0005
```

<details class="pt"><summary>延伸</summary>

生成器还有一个隐含陷阱：它是惰性的，错误和副作用推迟到被消费时才发生。把读文件的生成器返回给调用方，文件可能在读完之前就被关掉。

</details>

**知识点：**减少分配（Reducing Allocation）
