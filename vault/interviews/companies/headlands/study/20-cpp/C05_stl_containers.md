# C05 · STL 容器：复杂度、内存布局、迭代器失效

> 目标：对每个容器说得出「内部长什么样、操作复杂度、什么操作让迭代器/引用失效」。这是 C++ 面试的高频追问，也是写出快代码的基础。

## 1. Java 对照

| Java | C++ | 关键区别 |
|---|---|---|
| `ArrayList<T>` | `std::vector<T>` | C++ 存的是 **T 本身**（连续内存），Java 存引用 |
| `ArrayDeque` | `std::deque<T>` | 分块数组 |
| `LinkedList` | `std::list<T>` | 双向链表，每节点一次分配 |
| `HashMap` | `std::unordered_map` | 链式桶；节点稳定 |
| `TreeMap` | `std::map` | 红黑树，按 key 有序 |
| `HashSet`/`TreeSet` | `unordered_set` / `set` | 同上 |
| `int[]` / 固定数组 | `std::array<T,N>` | 大小是类型的一部分，无堆分配 |
| `PriorityQueue` | `std::priority_queue` | 默认**大顶堆**（Java 是小顶堆） |

**迭代器（iterator）** = 指向容器元素的"广义指针"，`begin()` 指向第一个，`end()` 指向**最后一个之后**。**失效（invalidation）** = 容器变化后，旧的迭代器/指针/引用不再有效，使用它是未定义行为（Java 会抛 `ConcurrentModificationException`，C++ 不检查）。

## 2. 复杂度与布局速查

| 容器 | 布局 | 随机访问 | 尾部插入 | 中间插入/删除 | 查找 |
|---|---|---|---|---|---|
| `vector` | 一整块连续内存 | O(1) | 摊销 O(1) | O(n) 搬移 | O(n)，有序时二分 O(log n) |
| `deque` | 固定大小块的数组 | O(1) | 首尾摊销 O(1) | O(n) | O(n) |
| `list` | 双向链表节点 | 否 | O(1) | 已有迭代器时 O(1) | O(n) |
| `map` / `set` | 红黑树节点 | 否 | O(log n) | O(log n) | O(log n)，有序遍历 |
| `unordered_map` / `set` | 桶数组 + 链 | 否 | 平均 O(1) | 平均 O(1) | 平均 O(1)，最坏 O(n) |
| `array` | 内联，大小固定 | O(1) | — | — | O(n) |

## 3. `vector`

```cpp
void growth() {
    std::vector<int> v;
    std::size_t last_cap = v.capacity();
    std::cout << "  capacity trace (push_back 0..1000):";
    int reallocations = 0;
    for (int i = 0; i < 1000; ++i) {
        v.push_back(i);
        if (v.capacity() != last_cap) {          // each change = new block allocated, elements moved, old block freed
            last_cap = v.capacity();
            ++reallocations;
            if (reallocations <= 12) std::cout << " " << last_cap;
        }
    }
    std::cout << " ... total " << reallocations << " reallocations\n";
    std::vector<int> r;
    r.reserve(1000);
    for (int i = 0; i < 1000; ++i) r.push_back(i);
    std::cout << "  with reserve(1000): capacity " << r.capacity() << ", reallocations 0\n";
}
```

```cpp
void erase_idioms() {
    std::vector<int> v{5, 3, 8, 3, 9, 3, 1};
    v.erase(std::remove(v.begin(), v.end(), 3), v.end());          // erase-remove idiom (C++20: std::erase(v, 3))
    std::cout << "  after erase-remove(3):";
    for (int x : v) std::cout << " " << x;
    std::cout << "\n";
    std::vector<int> w{1, 2, 3, 4, 5, 6};
    std::erase_if(w, [](int x) { return x % 2 == 0; });            // C++20
    std::cout << "  after erase_if(even):";
    for (int x : w) std::cout << " " << x;
    std::cout << "\n";
}
```

```cpp
void vector_bool_trap() {
    std::vector<bool> flags(10);
    auto first = flags[0];            // NOT a bool&: a proxy object that points into a bit-packed word
    flags[0] = true;
    std::cout << "  vector<bool>::operator[] returns a proxy; the proxy taken before the write now reads " << static_cast<bool>(first)
              << " (it aliases the vector, it is not a copy)\n";
    // bool* p = &flags[0];           // does not compile: there is no address of a bit
}
```

```text
  capacity trace (push_back 0..1000): 1 2 4 8 16 32 64 128 256 512 1024 ... total 11 reallocations
  with reserve(1000): capacity 1000, reallocations 0
  after erase-remove(3): 5 8 9 1
  after erase_if(even): 1 3 5
  vector<bool>::operator[] returns a proxy; the proxy taken before the write now reads 1 (it aliases the vector, it is not a copy)
  sizeof(std::array<int,4>)=16 (exactly 4 ints, no header, no pointer)
  sizeof(std::vector<int>)=24 (three pointers: begin, end, end-of-capacity)
```

* `vector` 对象本身只有三个指针（begin、end、end-of-capacity），24 字节；元素在堆上的连续块里。容量不够时：分配更大的块（常见增长因子 1.5–2）→ 移动旧元素 → 释放旧块，所以 **`push_back` 摊销 O(1)**，但可能触发整体搬移。已知大小就 `reserve`，省掉所有重分配。
* 删除元素用 erase-remove 惯用法，C++20 有 `std::erase` / `std::erase_if`。
* `vector<bool>` 是按位压缩的特例，`operator[]` 返回代理对象，不是 `bool&`，别用。
* `string`：同样是连续字符块，且有**小字符串优化（SSO）**：

```cpp
bool is_inline(const std::string& s) {             // does the character buffer live inside the string object itself?
    auto b = reinterpret_cast<std::uintptr_t>(&s);
    auto d = reinterpret_cast<std::uintptr_t>(s.data());
    return d >= b && d < b + sizeof(std::string);
}

void sso() {
    std::cout << "  sizeof(std::string)=" << sizeof(std::string) << ", capacity of an empty string=" << std::string().capacity() << "\n";
    for (std::size_t n : {5, 22, 23, 40}) {
        std::string s(n, 'x');
        std::cout << "  length " << n << ": characters " << (is_inline(s) ? "INSIDE the object (no allocation)" : "on the HEAP") << "\n";
    }
}
```

```text
  sizeof(std::string)=24, capacity of an empty string=22
  length 5: characters INSIDE the object (no allocation)
  length 22: characters INSIDE the object (no allocation)
  length 23: characters on the HEAP
  length 40: characters on the HEAP
```

这个实现里 ≤22 字节的字符串直接存在 24 字节的 `string` 对象内部，不分配堆内存（不同标准库阈值不同，GCC 是 15）。

## 4. 迭代器失效规则（必背）

| 容器 | 插入 | 删除 |
|---|---|---|
| `vector` | 重分配时**全部**失效；否则插入点之后失效 | 被删位置及之后失效 |
| `deque` | 两端插入：**迭代器**失效，**引用/指针**不失效；中间插入全部失效 | 中间删除全部失效；两端删除只影响被删元素 |
| `list` | 都不失效 | 只有被删元素失效 |
| `map`/`set` | 都不失效 | 只有被删元素失效 |
| `unordered_*` | rehash 时**迭代器**失效，**引用/指针**不失效；否则不失效 | 只有被删元素失效 |

用地址验证上表：

```cpp
{
    std::vector<int> v{1, 2, 3};      // capacity == size: the next push_back must reallocate
    std::cout << "vector push_back at full capacity     : first element kept its address? "
              << same_address_after(v, [](auto& c) { c.push_back(4); }, [](auto& c) { return &c.front(); }) << "\n";
    std::vector<int> r{1, 2, 3}; r.reserve(100);
    std::cout << "vector push_back with spare capacity  : first element kept its address? "
              << same_address_after(r, [](auto& c) { c.push_back(4); }, [](auto& c) { return &c.front(); }) << "\n";
    std::deque<int> d{1, 2, 3};
    std::cout << "deque push_back x1000                 : first element kept its address? "
              << same_address_after(d, [](auto& c) { for (int i = 0; i < 1000; ++i) c.push_back(i); }, [](auto& c) { return &c.front(); })
              << "  (iterators ARE invalidated, references are not)\n";
    std::list<int> l{1, 2, 3};
    std::cout << "list push_back x1000                  : first element kept its address? "
              << same_address_after(l, [](auto& c) { for (int i = 0; i < 1000; ++i) c.push_back(i); }, [](auto& c) { return &c.front(); }) << "\n";
    std::map<int, int> m{{1, 1}, {2, 2}};
    std::cout << "map insert x1000                      : first element kept its address? "
              << same_address_after(m, [](auto& c) { for (int i = 10; i < 1010; ++i) c[i] = i; }, [](auto& c) { return &c.begin()->second; }) << "\n";
    std::unordered_map<int, int> u{{1, 1}, {2, 2}};
    auto buckets0 = u.bucket_count();
    std::cout << "unordered_map insert x1000 (rehash)   : first element kept its address? "
              << same_address_after(u, [](auto& c) { for (int i = 10; i < 1010; ++i) c[i] = i; }, [](auto& c) { return &c.find(1)->second; })
              << "  (bucket_count " << buckets0 << " -> " << u.bucket_count() << ", iterators invalidated by rehash, references not)\n";
}
```

```text
vector push_back at full capacity     : first element kept its address? false
vector push_back with spare capacity  : first element kept its address? true
deque push_back x1000                 : first element kept its address? true  (iterators ARE invalidated, references are not)
list push_back x1000                  : first element kept its address? true
map insert x1000                      : first element kept its address? true
unordered_map insert x1000 (rehash)   : first element kept its address? true  (bucket_count 2 -> 1597, iterators invalidated by rehash, references not)
```

典型 bug：持有 `vector` 元素的引用，再 `push_back`：

```cpp
// C05: iterator/reference invalidation. push_back may reallocate; every iterator, pointer and reference into the old block dangles.
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v{1, 2, 3};
    int& first = v[0];              // reference into the current buffer
    auto it = v.begin();            // iterator into the same buffer
    v.push_back(4);                 // capacity was 3: reallocation, old buffer freed
    std::cout << "size=" << v.size() << "\n";
    std::cout << first << "\n";     // use-after-free (ASan: heap-use-after-free)
    std::cout << *it << "\n";
}
```

```text
ERROR: AddressSanitizer: heap-use-after-free on address 0x… at pc 0x… bp 0x… sp 0x…
READ of size 4 at 0x… thread T0
0x… is located 0 bytes inside of 12-byte region [0x…,0x…)
freed by thread T0 here:
previously allocated by thread T0 here:
SUMMARY: AddressSanitizer: heap-use-after-free (c05_invalidation_ub:arm64+0x…) in main+0x474
```

正确的"边遍历边删除"写法：用 `erase` 的返回值（指向下一个有效元素）：

```cpp
{
    std::vector<int> v{1, 2, 3, 4, 5, 6};
    for (auto it = v.begin(); it != v.end();) {     // the correct erase-while-iterating loop
        if (*it % 2 == 0) it = v.erase(it);         // erase returns the NEXT valid iterator
        else ++it;
    }
    std::cout << "vector erase loop, odds left:";
    for (int x : v) std::cout << " " << x;
    std::cout << "\n";

    std::map<int, int> m{{1, 10}, {2, 20}, {3, 30}, {4, 40}};
    for (auto it = m.begin(); it != m.end();) {
        if (it->first % 2 == 0) it = m.erase(it);   // node containers: only the erased element's iterator dies
        else ++it;
    }
    std::cout << "map erase loop, keys left:";
    for (auto& [k, val] : m) std::cout << " " << k << "=" << val;
    std::cout << "\n";
}
```

```text
vector erase loop, odds left: 1 3 5
map erase loop, keys left: 1=10 3=30
```

## 5. `unordered_map`：桶与 rehash

标准库实现是**链式哈希**：一个桶数组，key 的哈希值取模选桶，桶里是链表；每个元素是单独分配的节点，所以引用稳定。**负载因子（load factor）** = 元素数 / 桶数，超过 `max_load_factor`（默认 1.0）就 **rehash**：桶数增加（约翻倍并取素数），所有元素重新分桶，**迭代器失效**。

```cpp
void rehash_trace() {
    std::unordered_map<int, int> m;
    std::size_t last = m.bucket_count();
    std::cout << "  initial bucket_count=" << last << " max_load_factor=" << m.max_load_factor() << "\n  rehash points:";
    for (int i = 0; i < 100000; ++i) {
        m[i] = i;
        if (m.bucket_count() != last) { last = m.bucket_count(); std::cout << " " << m.size() << "->" << last; }
    }
    std::cout << "\n  final size=" << m.size() << " buckets=" << m.bucket_count() << " load_factor=" << m.load_factor() << "\n";
    std::unordered_map<int, int> r;
    r.reserve(100000);                                    // pre-size: zero rehashes during the fill
    std::size_t b = r.bucket_count();
    for (int i = 0; i < 100000; ++i) r[i] = i;
    std::cout << "  with reserve(100000): buckets " << b << " before and " << r.bucket_count() << " after the fill\n";
}
```

```cpp
struct Key {
    std::uint32_t exch;
    std::string sym;
    bool operator==(const Key& o) const { return exch == o.exch && sym == o.sym; }
};
struct KeyHash {
    std::size_t operator()(const Key& k) const {
        std::size_t h = std::hash<std::string>{}(k.sym);
        return h ^ (std::hash<std::uint32_t>{}(k.exch) + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2));   // boost-style combine
    }
};
```

```cpp
struct BadHash { std::size_t operator()(int) const { return 42; } };    // every key collides: O(n) per operation
```

```text
[rehash]
  initial bucket_count=0 max_load_factor=1
  rehash points: 1->2 3->5 6->11 12->23 24->47 48->97 98->197 198->397 398->797 798->1597 1598->3203 3204->6421 6422->12853 12854->25717 25718->51437 51438->102877
  final size=100000 buckets=102877 load_factor=0.972035
  with reserve(100000): buckets 100003 before and 100003 after the fill
[buckets and collisions]
  20 keys in 23 buckets, longest chain 1
[custom key]
  (1,AAPL)=125 (2,AAPL)=50 entries=2
[all keys collide]
  1000 ints with a constant hash: longest chain 1000 (lookups degrade to a linear scan)
[operator[] inserts]
  value 0, size now 1; find() leaves it alone: 1, size 1
```

* 已知元素数就 `reserve(n)`：一次建好桶，填充期间零 rehash。
* 自定义 key 需要 `operator==` 加一个哈希函数对象；哈希质量差（极端：全相同）会退化为 O(n) 的链表扫描。
* **`operator[]` 会插入**默认值，只想查用 `find`/`contains`。
* Java 的 `HashMap` 桶链过长会转红黑树；`std::unordered_map` 不会，最坏仍是 O(n)。

## 6. `map` / `set`：红黑树

有序、O(log n)、每个元素一个堆节点（payload + 父/左/右指针 + 颜色）。`begin()` 是最小 key，`rbegin()` 是最大，`lower_bound(k)` 返回第一个 **不小于** k 的元素。订单簿一侧天然适合：

```cpp
// Order book side: price -> total quantity. std::map is sorted, so best bid/ask are O(1) at the ends, lookups O(log n).
void order_book() {
    std::map<long, long, std::greater<long>> bids;     // descending: begin() is the best (highest) bid
    std::map<long, long> asks;                         // ascending : begin() is the best (lowest) ask
    bids[10010] += 100; bids[10005] += 50; bids[10010] += 25; bids[9990] += 300;
    asks[10020] += 40;  asks[10030] += 10; asks[10025] += 75;
    std::cout << "  best bid " << bids.begin()->first << " x " << bids.begin()->second
              << ", best ask " << asks.begin()->first << " x " << asks.begin()->second << "\n";
    auto it = bids.lower_bound(10006);                 // first key NOT BEFORE 10006 in this ordering (<= 10006 here)
    std::cout << "  first bid at or below 10006: " << it->first << "\n";
    std::cout << "  asks in [10020,10026]:";
    for (auto i = asks.lower_bound(10020); i != asks.upper_bound(10026); ++i) std::cout << " " << i->first;
    std::cout << "\n";
    if (auto f = asks.find(10025); f != asks.end()) asks.erase(f);     // erase by iterator: O(1) amortised
    std::cout << "  asks left: " << asks.size() << "\n";
}
```

```text
  best bid 10010 x 125, best ask 10020 x 40
  first bid at or below 10006: 10005
  asks in [10020,10026]: 10020 10025
  asks left: 2
```

买盘用 `std::greater` 让最高价排最前，所以 `begin()` 永远是最优价。

## 7. 内存布局的实际代价

对 200 万个 `int` 求和，复杂度都是 O(n)：

链表节点在内存里按分配顺序排；先乱序分配、再 `sort()`（只重连节点，不搬节点）就得到"遍历顺序与内存顺序无关"的链表，模拟长期运行后的堆：

```cpp
std::list<int> l_shuffled;                             // nodes allocated in shuffled value order ...
for (int x : order) l_shuffled.push_back(x);
l_shuffled.sort();                                     // ... then RELINKED in value order: traversal jumps around memory
```

求和（每元素纳秒）：

```text
sum over 2000000 ints, ns per element
  vector           : 0.0421834 ns/element (checksum 9999995000000)
  deque            : 0.239563 ns/element (checksum 9999995000000)
  list (alloc seq.): 0.781017 ns/element (checksum 9999995000000)
  list (shuffled)  : 63.5815 ns/element (checksum 9999995000000)
  set (RB-tree)    : 2.46063 ns/element (checksum 9999995000000)
  unordered_map    : 0.897646 ns/element (checksum 9999995000000)
```

读法：`vector` 是连续内存，硬件预取器和 SIMD 都能发挥，每元素远低于 1 ns；节点按顺序分配的 `list`/`unordered_map` 尚可；**乱序的 `list` 每个元素一次缓存未命中**，慢两个数量级；`set` 居中。这就是"默认用 `vector`"的依据：同样的 O(n)，常数差 10–1000 倍。

## 8. 坑

1. **持有 `vector` 元素的引用/迭代器再 `push_back`**（上例）：UB。需要稳定地址就 `reserve` 够、用 `deque`/`list`、或存下标。
2. **`for` 循环里 `erase` 当前元素后继续 `++it`**：`erase` 之后 `it` 已失效，要用 `it = v.erase(it)`。
3. **`map::operator[]` 查询会插入**，让 `size()` 变化，也破坏 `const` 正确性（`const map` 上没有 `operator[]`）。
4. **`vector<int> v(n)` 与 `vector<int> v{n}`**：圆括号是 n 个元素，花括号是一个值为 n 的元素。
5. **`unordered_map` 遍历顺序不确定**，不要依赖；需要有序用 `map`。
6. **`std::sort` 比较器必须是严格弱序**：用 `<=` 会在相等元素上越界崩溃。
7. 中间频繁插入删除时，`vector` 的 O(n) 搬移通常仍比 `list` 的缓存未命中快，除非元素很大或必须保持迭代器稳定。

## 9. 面试官接着会问

**Q：`vector` 扩容怎么工作？复杂度？**
要点：容量翻倍（因子取决于实现）；分配新块、移动（或拷贝）元素、释放旧块；摊销 O(1)；`reserve` 避免；扩容让所有迭代器/引用失效；移动构造 `noexcept` 才被使用。

**Q：`unordered_map` 怎么实现？什么时候最坏？**
要点：桶数组 + 链；负载因子触发 rehash；平均 O(1)、最坏 O(n)（哈希碰撞）；rehash 使迭代器失效但元素地址稳定；要 `reserve`；缓存不友好（节点分配），热路径常换成开放寻址哈希表。

**Q：`map` 与 `unordered_map` 怎么选？**
要点：要有序遍历/范围查询/`lower_bound`/最小最大 → `map`；只要点查 → `unordered_map`；元素很少时排好序的 `vector` + 二分往往最快。

**Q：什么操作使迭代器失效？**
要点：第 4 节表格，重点 `vector` 重分配、`unordered` rehash、`erase` 返回下一个迭代器。

**Q：`deque` 是什么？**
要点：分块数组，两端 O(1) 插入，随机访问 O(1)（两次间接），元素不连续，两端插入不使引用失效。

**Q：`string` 的 SSO？**
要点：短字符串存在对象内部的缓冲区，省一次堆分配；阈值依实现；`string` 移动后源对象是否为空取决于是否在 SSO 内。

**Q：`std::array` 与 C 数组？**
要点：`array` 是带 `size()`/迭代器/拷贝语义的零开销封装，不退化为指针。

## 10. 自测

1. 什么时候 `v.push_back(x)` 之后 `v[0]` 的地址不变？
2. `unordered_map` rehash 之后，旧迭代器和旧的元素引用，哪个还能用？
3. 为什么乱序的 `std::list` 遍历特别慢？
4. 订单簿里最优卖价如何 O(1) 取到？

<details><summary>答案</summary>

1. 容量有余（`size < capacity`）时不重分配，地址不变。
2. 引用/指针仍有效（节点没有被搬动），迭代器失效。
3. 节点散落在堆里，每步一次指针追逐 = 一次缓存未命中，无法预取。
4. 卖盘用 `std::map<price, qty>`（升序），`begin()` 就是最低卖价；买盘用 `std::greater` 排序或 `rbegin()`。

</details>
