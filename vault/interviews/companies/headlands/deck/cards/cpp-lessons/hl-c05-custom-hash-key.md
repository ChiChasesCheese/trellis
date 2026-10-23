---
id: hl-c05-custom-hash-key
node: cpp-lessons.c05-stl-containers
type: qa
step: 15
---
## Q
怎么让自定义结构体 `Key{uint32_t exch; std::string sym;}` 做 `unordered_map` 的键？哈希质量差会怎样？

## A
需要两样东西：`operator==` 和一个哈希函数对象，并把它作为第二个模板参数。

```cpp
struct Key {
    std::uint32_t exch; std::string sym;
    bool operator==(const Key& o) const { return exch == o.exch && sym == o.sym; }
};
struct KeyHash {
    std::size_t operator()(const Key& k) const {
        std::size_t h = std::hash<std::string>{}(k.sym);
        return h ^ (std::hash<std::uint32_t>{}(k.exch)
                    + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2));  // boost 风格组合
    }
};
```
- 哈希质量差会退化：实测 1000 个 `int` 用常量哈希，最长链 1000，查找退化为线性扫描 O(n)。
- Java 的 `HashMap` 桶链过长会转红黑树；`unordered_map` 不会。
