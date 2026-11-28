---
id: lct-learn-math-6-1
node: math.6.1
type: qa
step: 1
---
## Q
**数学算法 › 随机算法 › 随机数**｜学习卡

套路是什么？

## A
**一句话。** 随机题都是把「等概率」落到整数上：先造出一个均匀的整数，再映射回目标（前缀和 + 二分、洗牌换位、取模、拒绝采样）。

下图：LC 528（w = [1,3,2]），每段长度等于权重，均匀整数落进哪段就选哪个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="30" y="50" width="45" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="52.5" y="70" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">0</text>
<text x="52.5" y="96" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">w = 1</text>
<rect x="75" y="50" width="135" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="142.5" y="70" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">下标 1</text>
<text x="142.5" y="96" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">w = 3</text>
<rect x="210" y="50" width="90" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="255.0" y="70" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">下标 2</text>
<text x="255.0" y="96" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">w = 2</text>
<text x="75" y="112" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s = 1</text>
<text x="210" y="112" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s = 4</text>
<text x="300" y="112" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s = 6</text>
<line x1="143" y1="26" x2="143" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="143.0,48.0 140.0,41.7 146.0,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="143" y="20" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">x = 3</text>
<text x="170" y="134" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">均匀抽 x ∈ [1, 总和]，bisect_left(前缀和, x) 落在第几段</text>
</svg>

```python
class Pick:                          # 按权重随机：前缀和 + 二分
    def __init__(self, w):
        self.s = list(accumulate(w))
    def pick(self):
        x = random.randint(1, self.s[-1])   # 均匀整数 1..总和
        return bisect_left(self.s, x)       # 落在第几段

def shuffle(a):                      # Fisher-Yates 洗牌
    for i in range(len(a)):
        j = random.randint(i, len(a) - 1)   # 在 [i, n) 里选
        a[i], a[j] = a[j], a[i]
    return a
```

**要点。**
- 为什么对？：洗牌时第 `i` 位在剩下 `n - i` 个里等概率选，所有排列概率都是 `1 / n!`；权重则是总和长度的数轴上等概率落点，段越长概率越大。
- LC 470 怎么改？：拒绝采样：`(rand7() - 1) * 7 + rand7()` 等概率落在 `1..49`，只收 `<= 40` 的，再 `% 10 + 1`，其余重来。
- LC 478 怎么改？：半径取 `R * sqrt(random())`，角度均匀取 `[0, 2π)`；半径直接均匀取会让圆心附近过密。
- LC 380 / 381 怎么改？：数组存元素供随机取，字典存值到下标；删除时用末尾元素填坑再弹出，保持数组紧凑；381 的字典值是下标集合。

**易错点。**
- 洗牌选范围用 `[0, n)`：`[1,2,3]` 会得到 `n^n` 种等可能路径，不能均分 `n!` 种排列。
- 拒绝采样用取模凑数：`49 % 10` 会让 `1..9` 比 `10` 多一份，必须丢掉 `41..49`。
- 380 删除的恰好是末尾元素：先改字典再弹出，顺序反了会留下脏下标。

**对应题目。** LC 478 在圆内随机生成点、LC 470 用 Rand7() 实现 Rand10()、LC 381 O(1) 时间插入、删除和获取随机元素 - 允许重复、LC 380 O(1) 时间插入、删除和获取随机元素、LC 528 按权重随机选择、LC 384 打乱数组
