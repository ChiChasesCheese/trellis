---
id: ai-specs-numbers-beat-adjectives
node: ai.specs
type: qa
step: 2
---
## Q
“每分钟最多 3 次”这句话，两个人写出了不同的限流器，而且都说自己符合要求。差别出在哪？用什么消除分歧？

## A
**一个数字例子比一句形容词更能定下行为**

- **固定窗口**：按整分钟划桶，每个桶最多 3 次；
- **滑动窗口**：任何一个 60 秒的区间内最多 3 次；
- **分歧在哪**：两种都满足这句话，在桶的边界附近行为不同；
- **消除办法**：写一条跨边界的例子，规定每个时刻的结果；有了它，实现只剩一种。

```python
def fixed(hits, t):                 # 按整分钟分桶
    return sum(h // 60 == t // 60 for h in hits) < 3

def sliding(hits, t):               # 任意 60 秒区间
    return sum(t - h < 60 for h in hits) < 3

hits = [50, 55, 58]                 # 已放行三次
print(fixed(hits, 61), sliding(hits, 61))    # True False
```

<details class="pt"><summary>延伸</summary>

固定窗口在边界两侧能放行接近两倍的请求，滑动窗口不会，但要记下每次请求的时刻。这个取舍是设计决定，写进指令，而不是留给实现去选。

</details>

**知识点：**写清任务（Specifying the Task）
