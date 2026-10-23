---
id: hl-cx-arraylist-growth
node: foundations.complexity
type: qa
step: 22
---
## Q
`ArrayList.add` 单次最坏要复制 n 个元素，为什么大家仍说它是 O(1)？容量翻倍时前 16 次 add 的总代价是多少？

## A
`ArrayList` 底层是长度固定的 `Object[]`，满了就分配更大的新数组并全部抄过去，这一次 add 是 O(n)。若每次 add 都这样，n 次就是 O(n²)。

之所以说 O(1)，是因为扩容时**容量成倍增长**，下一次扩容要等很久。容量每次翻倍时，贵的 add 出现在第 2、3、5、9、17、33 次……间隔翻倍。前 16 次 add：写 16 次 + 抄 (1+2+4+8) = 15 次 = 31，平均每次约 2，所以摊还 O(1)。
