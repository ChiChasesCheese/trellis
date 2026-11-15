---
slug: linked-list-random-node
---
## Q
**LC 382 链表随机节点**｜Medium

给单链表，设计 `getRandom()`：每次等概率随机返回一个节点的值，链表长度未知且可能很长。

## A
**一句话。** 水塘抽样：一遍扫链表，第 `i` 个节点以 `1/i` 的概率顶替当前答案，最后每个节点被选中的概率都是 `1/n`。

```python
class Solution:
    def __init__(self, head):
        self.head = head

    def getRandom(self):
        ans, cur, i = 0, self.head, 0
        while cur:
            i += 1
            if random.randrange(i) == 0:   # 以 1/i 换入
                ans = cur.val
            cur = cur.next
        return ans
```

**复杂度。** 时间每次 `O(n)`，空间 `O(1)`。

**易错点。**
- 先统计长度再 `randint`：长度未知又不许多遍扫描时做不到，这正是要用抽样的原因。
- 先抽后 `i += 1`：`randrange(0)` 会报错，计数要先加。
- 概率写成固定 `1/2`：越往后越难被选，要用 `1/i`。

**追问。**
- 为什么概率相等？：第 `k` 个被选中的概率是 `1/k`，之后每步不被换掉的概率 `(i-1)/i`，连乘得 `1/n`。
- 一次抽 `m` 个怎么办？：前 `m` 个直接入池，之后第 `i` 个以 `m/i` 的概率随机换掉池中一个。

**同模式。** LC 398 随机数索引、LC 528 按权重随机选择、LC 497 非重叠矩形中的随机点、LC 478 在圆内随机生成点
