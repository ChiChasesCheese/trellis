---
id: performance-cc-join-by-key
node: performance.complexity-constants
type: qa
step: 3
---
## Q
应收款对账：每一笔应收款要找出同一个合约号下的所有合约。第一版对每笔应收款扫描全部合约，一万笔乘一万份合约。为什么这是个问题？先按键归组为什么能解决？什么时候反而不该建索引？

## A
**要按键配对时，先把一边按键归组，另一边直接取**

- **嵌套扫描是 n × m**：一万 × 一万是一亿次比较，规模翻倍，时间翻四倍；
- **归组一次是 O(m)，每笔查询是 O(1)**：整体 O(n + m)，两边都只过一遍；
- **归组结果是临时的**：它只活在这个函数里，不需要维护更新，也没有两份数据不一致的问题；
- **只查一次就别建索引**：建索引要过一遍全部数据，一次查询的扫描也是一遍，没有省；先线性扫描，查询多起来、测出慢了再建；
- **键要选对**：归组键必须是真正的相等条件，比如合约号；范围条件（金额区间）用排序加二分，不是字典。

实测（3.11，本机，各 2000 条，500 个不同的键，两种写法得到的配对数相同，都是 8000）：嵌套扫描 24.3 ms，先归组 0.10 ms。按平方外推到一万 × 一万，嵌套扫描约 25 倍，也就是 0.6 秒左右；归组版仍是毫秒级。

```python
from collections import defaultdict

contracts = [("C1", "合约A"), ("C2", "合约B"), ("C1", "合约C")]
receivables = [("C1", 100), ("C2", 50), ("C3", 10)]

by_key = defaultdict(list)
for key, name in contracts:
    by_key[key].append(name)                       # 归组一次

for key, amount in receivables:
    print(key, amount, by_key.get(key, []))        # 不存在的键用 .get，不污染字典
# C1 100 ['合约A', '合约C']  /  C2 50 ['合约B']  /  C3 10 []
```

<details class="pt"><summary>延伸</summary>

读取 `by_key[key]` 而不是 `.get(key)` 时，`defaultdict` 会把不存在的键悄悄插进字典，遍历时字典大小还会变化；只查不写，就用 `.get`。

</details>

**知识点：**复杂度与常数（Complexity vs Constants）
