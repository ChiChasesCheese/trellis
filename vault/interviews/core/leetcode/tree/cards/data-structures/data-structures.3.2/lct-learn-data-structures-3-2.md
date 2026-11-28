---
id: lct-learn-data-structures-3-2
node: data-structures.3.2
type: qa
step: 1
---
## Q
**常用数据结构 › 栈 › 进阶**｜学习卡

套路是什么？

## A
**一句话。** 进阶的栈让每个元素携带「入栈时的快照」（或延后结算的欠账），弹栈时快照自动消失，不需要撤销；最小栈就是每格存「到这格为止的最小值」。

下图：每格存「值 + 入栈时的最小值」快照；弹栈后下面那格的快照自动生效。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="140" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">值</text>
<text x="200" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">到此为止的最小</text>
<rect x="110" y="150" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="150" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="200" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">inf</text>
<text x="100" y="169" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哨兵</text>
<rect x="110" y="116" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="116" width="60" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="140" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="200" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="100" y="135" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">push 5</text>
<rect x="110" y="82" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="82" width="60" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="140" y="101" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="200" y="101" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="100" y="101" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">push 3</text>
<rect x="110" y="48" width="60" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="170" y="48" width="60" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="140" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="200" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="100" y="67" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">push 7</text>
<line x1="290" y1="47" x2="234" y2="47" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="234.0,47.0 240.3,44.0 240.3,50.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="296" y="44" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">get_min</text>
<text x="296" y="58" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 3</text>
<text x="170" y="200" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">pop 7 后，下一格自带最小值 3</text>
</svg>

```python
class MinStack:                      # LC 155
    def __init__(self):
        self.st = [(0, inf)]         # 哨兵：空栈的最小值是 inf

    def push(self, x):
        self.st.append((x, min(x, self.st[-1][1])))   # 带快照

    def pop(self):
        self.st.pop()

    def top(self):
        return self.st[-1][0]

    def get_min(self):
        return self.st[-1][1]        # 栈顶快照就是当前最小
```

**要点。**
- 为什么对？：第 `i` 格的快照是前 `i` 个元素的最小值，弹出栈顶后剩下的栈与它入栈前完全一样，快照也一样，不用重算；任何能增量计算的聚合（`min`、`max`、和）都能这样存，全 `O(1)`。
- LC 1381 怎么改？：`increment(k, val)` 把欠账只记在第 `min(k, 栈长)` 格，弹出时 `add[-1] += inc` 下传给下一格，返回 `值 + inc`。
- LC 636 怎么改？：栈存正在运行的函数；`start` 时先结算栈顶到 `t` 的时间（`t - prev`）再入栈，`end` 时结算 `t - prev + 1` 并令 `prev = t + 1`。
- LC 2434、LC 716 怎么改？：2434 栈当缓冲区，预处理后缀最小值 `suf`，每读入一个字符就弹出所有 `<= suf[i+1]` 的栈顶写到结果里；716 栈加最大堆共享带编号的元素，删除只记编号，浮到顶再丢（惰性删除）。

**易错点。**
- 只用一个变量记最小值：`push(-2), push(0), push(-3), pop()` 后 `getMin` 应得 `-2`，一个变量一直是 `-3`。
- LC 1381 欠账不下传：`push(1), push(2), increment(2,10)`，两次 `pop()` 应得 `12`、`11`。
- LC 636 `end` 漏掉 `+ 1`：`["0:start:0","1:start:2","1:end:5","0:end:6"]` 应得 `[3,4]`。

**对应题目。** LC 1381 设计一个支持增量操作的栈、LC 636 函数的独占时间（Exclusive Time of Functions）、LC 716 Max Stack、LC 155 最小栈、LC 2434 使用机器人打印字典序最小的字符串（Using a Robot to Print the Lexicographically Smallest String）
