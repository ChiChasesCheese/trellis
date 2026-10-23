---
id: hl-cx-collections-fast
node: foundations.complexity
type: qa
step: 11
---
## Q
Java 集合类 `ArrayList`、`HashMap`、`TreeMap`、`PriorityQueue`、`ArrayDeque`、`Collections.sort` 的常见操作复杂度分别是多少？

## A
- `ArrayList.get(i)` / `set(i, x)`：O(1)（数组下标）；`add(x)` 末尾：**摊还** O(1)。
- `HashMap.get/put/containsKey`：平均 O(1)，最坏 O(log n)（JDK 8+ 冲突桶树化）。
- `TreeMap.get/put/floorKey`：O(log n)（红黑树）。
- `PriorityQueue.offer/poll`：O(log n)（二叉堆）；`peek`：O(1)。
- `ArrayDeque.addLast/pollFirst`：摊还 O(1)（环形数组）。
- `Collections.sort` / `Arrays.sort(Object[])`：O(n log n)（TimSort，稳定）。
