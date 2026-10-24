---
id: pl-cpp-stl-ranges-found-invalidation
node: cpp.stl-ranges
type: qa
step: 4
---
## Q
迭代器失效（iterator invalidation）是什么？为什么 `vector` 扩容后旧迭代器不能再用，各容器的失效规则有什么规律？

## A
**定义**：容器被修改后，之前取得的迭代器、指针、引用可能不再指向有效的元素。继续使用它们是**未定义行为**。

**为什么会失效**：迭代器本质是元素的地址（或地址加簿记信息）。`vector` 的元素在一块连续内存里，容量不够时要申请更大的新块，把元素搬过去，释放旧块——所有指向旧块的迭代器、指针、引用都悬空了。

```cpp
std::vector<int> v{1,2,3};
int *p = &v[0];
v.push_back(4);        // 可能重新分配
println("{}", *p);     // ASan: heap-use-after-free ... READ of size 4
```

ASan 的真实报错：`AddressSanitizer: heap-use-after-free on address 0x602000000910`。

**规律（按布局推）**：
- **连续容器**（`vector`、`string`）：重新分配时全部失效；没重新分配时，插入/删除位置之后的失效；
- **节点容器**（`list`、`map`、`set`）：只有被删除的那个元素的迭代器失效，其余稳定（节点没搬动）；
- **哈希容器**（`unordered_map`）：**重新哈希**（rehash）时所有**迭代器**失效，但指向元素的**引用和指针仍然有效**（节点没搬动）。本机验证：对 `um[1]` 取引用，之后插入 1000 个元素触发重新哈希，引用仍读到 10；
- **`deque`**：中间插入删除全部失效，两端插入使迭代器失效但引用仍有效。

**最典型的错误：边遍历边删**：

```cpp
for (auto i = v.begin(); i != v.end(); ) {
  if (*i % 2 == 0) i = v.erase(i);   // erase 返回下一个有效迭代器
  else ++i;
}
```

写成 `v.erase(i); ++i;` 就是 UB。更好的做法是 **erase-remove 惯用法**（C++20 起用 `std::erase_if(v, pred)` 一行）。

**文档化而非检查**：失效规则写在标准里，但运行时不检查，除非用 ASan、libc++ 的调试模式。

**对比 Rust**：同样的代码在 Rust 里是编译错误：持有 `&v[0]` 的同时调用 `v.push(4)`，借用检查器报 `error[E0502]: cannot borrow 'v' as mutable because it is also borrowed as immutable`。Java 的容器在迭代时修改会抛 `ConcurrentModificationException`（运行时检查）；Python 对字典会报 `RuntimeError`。C++ 既不检查也不阻止。

**要记住的一点**：修改容器前，先想"我手里有哪些指向它的迭代器、指针、引用"，把它们当作作废。
