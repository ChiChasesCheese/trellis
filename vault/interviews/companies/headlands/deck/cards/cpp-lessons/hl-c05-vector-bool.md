---
id: hl-c05-vector-bool
node: cpp-lessons.c05-stl-containers
type: qa
step: 6
---
## Q
`std::vector<bool>` 有什么陷阱？

## A
- 它是**按位压缩**的特例（每个元素一个 bit）。
- `operator[]` 返回的是**代理对象**（proxy，指向压缩字里某一位），不是 `bool&`。
- 例：`auto first = flags[0]; flags[0] = true;` 之后 `first` 读出来是 `1`——它别名了 `vector`，不是拷贝。
- `bool* p = &flags[0];` 编译不过，因为没有"位的地址"。
- 结论：别用 `vector<bool>`。
