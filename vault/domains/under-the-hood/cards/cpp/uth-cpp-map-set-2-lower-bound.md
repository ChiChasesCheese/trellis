---
id: uth-cpp-map-set-2-lower-bound
node: cpp.map-set
type: qa
step: 2
---
## Q
**std::lower_bound 查 set 为什么慢了一万倍**｜C++ · std::set

对 `std::set` 做二分查找，写 `s.lower_bound(x)` 和 `std::lower_bound(s.begin(), s.end(), x)` 有什么区别？

## A
**结构。** 成员函数沿红黑树下降；全局算法只拿到双向迭代器，不能跳着走。

**细节。**

- 全局版比较次数虽然是 O(log n)，但要把迭代器一步一步挪，总共 O(n) 步
- 实测 20 万元素的 `set`，2000 次查询：成员版约 0.2 毫秒，全局版约 1.7 秒

**为什么。** 通用算法只依赖迭代器类别，不知道容器是树；成员函数才能利用树结构。

**坑。** 对 `set`、`map` 的二分一律用成员函数；只有 `vector` 这类随机访问容器才用全局版。

**对应 LeetCode：** LC 220 存在重复元素 III · LC 475 供暖器
