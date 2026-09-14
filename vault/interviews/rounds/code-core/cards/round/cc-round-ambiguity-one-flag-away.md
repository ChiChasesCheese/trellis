---
id: cc-round-ambiguity-one-flag-away
node: round.ambiguity
type: qa
---
## Q
You have picked one reading of an ambiguous rule and coded it. How do you keep the other reading cheap?

## A
**Put the decision in one named constant or parameter, used once.**

```python
STICKY = False   # spec ambiguous: does a flagged account recover after a reversal?
...
flagged = ever_flagged if STICKY else currently_flagged
```

Flipping the reading then costs one edit at a place you can find, not a hunt through three functions for the comparison you inlined. The name also documents the ambiguity for a reviewer and gives you something to say out loud. Do not build a general configuration layer — one flag per genuine ambiguity, and no flag for a rule the spec actually states.

## Q zh
你已经在一条含糊规则的两种读法里选了一种并写好了。怎样让另一种读法保持廉价？

## A zh
**把这个决定放进一个有名字的常量或参数，只用一次。**

```python
STICKY = False   # spec ambiguous: does a flagged account recover after a reversal?
...
flagged = ever_flagged if STICKY else currently_flagged
```

这样翻转读法只需在一个找得到的地方改一处，而不是在三个函数里找你内联进去的那个比较。这个名字同时向 reviewer 说明了歧义所在，也给了你可以说出口的话。不要造通用配置层 —— 每个真正的歧义一个 flag，题面已明说的规则不设 flag。
