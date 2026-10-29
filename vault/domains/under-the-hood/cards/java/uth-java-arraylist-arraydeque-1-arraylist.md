---
id: uth-java-arraylist-arraydeque-1-arraylist
node: java.arraylist-arraydeque
type: qa
step: 1
---
## Q
**ArrayList 怎么扩容**｜Java · OpenJDK 25

`new ArrayList<>()` 一路 `add`，底层数组的长度依次是多少？

## A
**结构。** 一个 `Object[] elementData` 加一个 `size`；满了就 `Arrays.copyOf` 到更大的新数组。

**细节。**

- 无参构造先共用一个空数组，第一次 `add` 才分配 10。
- 新容量 = 旧容量 + 旧容量 >> 1，即约 1.5 倍；实测依次是 `10 15 22 33 49 73 109 163 244`。
- `new ArrayList<>(n)` 或 `ensureCapacity(n)` 可预先分配，批量添加时省掉中间的多次复制。

**为什么。** 按比例增长保证均摊 O(1)；1.5 倍比 2 倍少浪费内存。CPython 的 `list` 更省，只多留约 12.5%。

**对应 LeetCode：** LC 380 O(1) 时间插入、删除和获取随机元素 · LC 1472 设计浏览器历史记录
