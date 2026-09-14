---
id: method-sequence-before-classes
node: method.modeling
type: qa
---
## Q
Why walk one concrete scenario ("car arrives → gets spot → ticket issued → ...") end-to-end *before* drawing the class diagram?

## A
The walkthrough forces every step onto some object, which exposes:

- **missing objects** — who computes the fee? who allocates the spot?
- **misplaced responsibilities** and the method signatures you actually need.

Class-diagram-first tends to produce data holders with no verbs; the gaps then surface mid-coding, when fixing them is most expensive.


## Q zh
为什么在**绘制类图之前**以一个具体的场景（"车到达 → 获得位置 → 票发出 → ..."）端到端走一遍?

## A zh
这个演练在某个对象上强制每一步，它暴露:

- **缺失的对象** — 谁计算费用? 谁分配位置?
- **误放的责任**以及你实际需要的方法签名。

类图优先的趋势是产生没有动词的数据持有者；差距然后在编码中期浮现，那时修复它们最昂贵。
