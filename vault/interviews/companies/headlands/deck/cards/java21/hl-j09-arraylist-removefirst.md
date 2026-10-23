---
id: hl-j09-arraylist-removefirst
node: java21.j09-sequenced-collections
type: qa
step: 27
---
## Q
为什么说"队列场景下用 `ArrayList.removeFirst()` 是个坑"？有什么数字？应该用什么？

## A
新 API 让 `list.removeFirst()` 和 `deque.removeFirst()` 一样顺手，**代价却完全不同**：`ArrayList` 是数组，删第一个要把后面所有元素前移 O(n)，循环出队 O(n²)。

20 万个元素逐个 `removeFirst()` 到空：
```
ArrayList.removeFirst x200000: 1147 ms;  ArrayDeque.removeFirst x200000: 1 ms
```
（机器相关，数量级才有意义：O(n²) 对 O(n)。）

当**队列**（FIFO）用，请用 **`ArrayDeque`**，别用 `ArrayList`。
