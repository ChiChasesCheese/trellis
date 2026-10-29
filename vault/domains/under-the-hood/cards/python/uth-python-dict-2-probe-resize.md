---
id: uth-python-dict-2-probe-resize
node: python.dict
type: qa
step: 2
---
## Q
**dict 的探测与扩容**｜Python · CPython 3.14

两个 key 落到同一个槽时，`dict` 怎么找下一个槽？表什么时候扩容？

## A
**结构。** 开放寻址（open addressing）：没有链表，冲突了就按公式换槽。

**细节。**

- 探测：`perturb >>= 5; i = (i*5 + perturb + 1) & mask`，`perturb` 初值是完整哈希值。
- 初始表长 8，最多用 2/3（8 槽放 5 个）；放满就按 `已用数 × 3` 向上取 2 的幂扩容。
- 实测 `getsizeof` 在放入第 1、6、11、22、43 个 key 时跳变。

**为什么。** 线性探测会让相邻哈希值挤成一团，`5*j+1` 走遍所有槽并打散聚集；留 1/3 空槽让探测很快结束。

**对应 LeetCode：** LC 1 两数之和 · LC 49 字母异位词分组
