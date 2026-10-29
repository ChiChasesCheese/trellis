---
id: uth-ai-autograd-1-record-replay
node: ai.autograd
type: qa
step: 1
---
## Q
**backward 怎么一次算出所有梯度**｜PyTorch · 2.14

模型有上亿个参数，`loss.backward()` 怎么一遍就算出每个参数的梯度？

## A
**背景。** 训练要知道：每个参数变一点点，损失（loss）会怎么变，这就是梯度。直觉做法是每个参数各微调一次、重算一遍损失，上亿个参数就要重算上亿遍。另一条路是链式法则（chain rule）：一连串运算的变化率，等于每一步的变化率相乘；每一步（加、乘、矩阵乘）的求导公式都很简单，难的是把它们接起来。

**结构。** 前向计算时，每做一次运算，PyTorch 就记下一个节点（`grad_fn`）：输入是谁、反向怎么算，连成一张有向无环图。`backward()` 从损失出发沿图往回走，每个节点把收到的梯度乘上自己的局部导数，传给它的输入。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<g font-size="12" font-family="sans-serif" text-anchor="middle" fill="currentColor" stroke="currentColor">
<rect x="8" y="28" width="44" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="30" y="47" stroke="none">a=2</text>
<rect x="8" y="168" width="44" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="30" y="187" stroke="none">b=3</text>
<circle cx="120" cy="112" r="16" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="120" y="116.2" stroke="none">×</text>
<circle cx="215" cy="70" r="16" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="215" y="74.2" stroke="none">+</text>
<rect x="282" y="56" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1"/>
<text x="307" y="75" stroke="none">d=8</text>
<line x1="52" y1="46" x2="106" y2="104" style="stroke-width:1"/>
<line x1="52" y1="178" x2="106" y2="122" style="stroke-width:1"/>
<line x1="136" y1="108" x2="202" y2="76" style="stroke-width:1"/>
<line x1="52" y1="38" x2="199" y2="66" style="stroke-width:1"/>
<line x1="231" y1="70" x2="282" y2="70" style="stroke-width:1"/>
<polygon points="106,104 99,101 104,96"/>
<polygon points="106,122 104,129 99,125"/>
<polygon points="202,76 197,82 194,76"/>
<polygon points="199,66 191,68 193,61"/>
<polygon points="282,70 275,74 275,66"/>
<text x="172" y="106" style="stroke:none;fill:var(--dim,#6b7280)">c=6</text>
<text x="257" y="62" font-weight="bold" style="stroke:none;fill:var(--accent,#3b6fd4)">1</text>
<text x="158" y="76" font-weight="bold" style="stroke:none;fill:var(--accent,#3b6fd4)">1</text>
<text x="120" y="52" font-weight="bold" style="stroke:none;fill:var(--accent,#3b6fd4)">1</text>
<text x="82" y="82" font-weight="bold" style="stroke:none;fill:var(--accent,#3b6fd4)">3</text>
<text x="82" y="160" font-weight="bold" style="stroke:none;fill:var(--accent,#3b6fd4)">2</text>
<text x="170" y="215" style="stroke:none;fill:var(--accent,#3b6fd4)">黑箭头是前向, 蓝字是反向传回的梯度</text>
<text x="170" y="234" stroke="none">a收到1和3, 相加得4; b收到2</text>
</g>
</svg>
```

**细节。**

- 图里 d = a×b + a，a = 2、b = 3，d 的梯度从 1 开始
- 乘法节点把 1 乘上另一个输入：a 得 3，b 得 2
- 加法节点把 1 原样传给 a；a 的两份 1 和 3 相加得 4，正是 d 对 a 的导数 b + 1

**为什么。** 反向走一遍，就得到所有输入的梯度；正向模式每个输入要各算一遍，每遍的代价约等于一次前向。参数很多、损失只有一个的训练，反向模式合算得多。

**对应 LeetCode：** 无直接对应的题
