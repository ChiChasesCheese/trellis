---
id: hl-j09-efficient-impls
node: java21.j09-sequenced-collections
type: qa
step: 17
---
## Q
JDK 对常用类的 Sequenced 方法是不是只靠 `default` 实现？`reversed()` 返回的是什么对象？

## A
不全靠 `default`，对常用类写了专门实现：
- `ArrayList` 重写了 `getFirst/getLast/removeFirst/removeLast/addFirst/addLast`，`getFirst` 直接读内部数组；
- `LinkedHashMap` 用内部链表实现 `putFirst/putLast/sequencedKeySet` 等，O(1)。

`reversed()` 各有对应的**视图类**（如 `ArrayList` 是 `ReverseOrderListView`，`LinkedHashMap` 是 `ReversedLinkedHashMapView`）。类名是实现细节，只说明它返回**包装现有数据的小对象**，不是拷贝。
