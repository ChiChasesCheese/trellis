---
id: tc-explaining-complexity
node: t03.explaining-complexity
type: qa
step: 1
tags: [原则]
---
## Q
**Explaining complexity · 从具体到抽象**｜原则 · 追问

你要给产品经理解释"最终一致性"。你一开口先讲了定义和三种例外，对方的眼神就空了。怎么讲？

## A
**原则：** 先给一个**具体**的例子，让对方有个落脚点；再抽象出规则；**例外**最后再说，或者干脆省掉。去掉一切对这位听众的决定没有影响的细节。

**怎么做：**
1. 先给一个具体的场景："You update your profile photo, but your friend still sees the old one for a few seconds."
2. 再用一句话抽象："That's eventual consistency: all copies agree, but not instantly."
3. 说明对对方的影响："So the feature will look right within seconds, but not in the same instant."
4. 例外只在对方要做的决定受它影响时才说。
5. 只用一个类比，用完就收。

**常见错法：**
- **先讲定义：** 对方还没有东西可以挂定义。
- **所有例外一起讲：** 听众记住例外，忘了规则。
- **用术语解释术语。**

**改写示例：**
- Before: "Eventual consistency means replicas converge under the absence of further updates, assuming no partitions…"
- After: "After you change something, other users might see the old version for a few seconds. Then everyone sees the new one."

<details class="pt" markdown="1"><summary>出处</summary>

Minto p. 113–136（Ch.7 Summarizing Grouped Ideas）（部分）；Google Technical Writing One《Audience》

</details>
