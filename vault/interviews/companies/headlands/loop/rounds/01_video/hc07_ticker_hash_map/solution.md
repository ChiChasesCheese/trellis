# hc07 · 解法与原理

这道优化题的主线只有一句话：key 的结构已知（至多 8 个大写字母），就别用通用的字符串。先把它变成一个整数，再围绕这个整数造一张紧凑的表。下面先说开场 3 分钟怎么做，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "A string key means a heap object, a pointer to chase and a comparison per probe. If a ticker is at most 8 uppercase letters, it fits in one 64-bit integer. Can I assume that? And do I need to support delete?"

面试官通常会说：只有 A–Z，最多 8 个，先不用删除。问出这几点，后面的取舍就有了依据。

## Part 1 · 打包成 64 位整数

**思路**：从左到右扫描字符，每读一个字符就把已有结果左移 8 位，再把字符放进最低字节。`decode` 反过来：每次取最低字节，右移 8 位，直到变成 0，最后把收集到的字符倒过来。

**原理：为什么这样做更快**

- 字符串 key 是一个堆上的对象：表里存的是指针，比较要先跳到别处，再逐字符比较，哈希要扫一遍字符。
- 打包后的 key 就是 8 字节整数：比较是一条指令，哈希是一次乘法，key 直接存在数组里，不分配，不用追指针。
- 8 个字符 × 8 位 = 64 位，刚好一个 `long`。字符是 `'A'..'Z'`（65..90），最高位永远是 0，所以合法 key 都 `> 0`；没有字节为 0，所以 `"A"` 和 `"AA"` 不会撞。0 因此可以当「空格」，不必另存一个标记数组。
- `decode` 必须检查每个字节在 A–Z 里：否则任何 `long` 都能被「解码」成乱码。

**Java**

```java
public static long encode(String ticker) {
    if (ticker.isEmpty() || ticker.length() > 8) throw new IllegalArgumentException("length must be 1..8: " + ticker);
    long key = 0;
    for (char c : ticker.toCharArray()) {
        if (c < 'A' || c > 'Z') throw new IllegalArgumentException("not A-Z: " + ticker);
        key = key << 8 | c;
    }
    return key;
}

public static String decode(long key) {
    if (key <= 0) throw new IllegalArgumentException("not a packed ticker: " + key);
    StringBuilder sb = new StringBuilder();
    for (; key != 0; key >>>= 8) {
        char c = (char) (key & 0xFF);
        if (c < 'A' || c > 'Z') throw new IllegalArgumentException("not a packed ticker");
        sb.append(c);
    }
    return sb.reverse().toString();
}
```

**C++**

```cpp
inline std::uint64_t encode(const std::string& ticker) {
    if (ticker.empty() || ticker.size() > 8) throw std::invalid_argument("length must be 1..8");
    std::uint64_t key = 0;
    for (char c : ticker) {
        if (c < 'A' || c > 'Z') throw std::invalid_argument("not A-Z");
        key = key << 8 | static_cast<std::uint64_t>(c);
    }
    return key;
}

inline std::string decode(std::uint64_t key) {
    if (key == 0) throw std::invalid_argument("not a packed ticker");
    std::string s;
    for (; key != 0; key >>= 8) {
        char c = static_cast<char>(key & 0xFF);
        if (c < 'A' || c > 'Z') throw std::invalid_argument("not a packed ticker");
        s.insert(s.begin(), c);
    }
    return s;
}
```

复杂度：时间 O(L)，L ≤ 8，空间 O(1)（`decode` 的结果字符串除外）。

## Part 2 · 开放寻址哈希表

**思路**：先写 `slot(key)`（key 落在哪一格），再写 `put`：从 `slot(key)` 开始向后找，直到碰到空格（key 为 0）或同一个 key；然后写 `get`，探测规则一样，碰到空格就说明不存在；最后写 `grow`。

**原理：几个关键决定**

- **开放寻址**：key 和 value 直接放在两个数组里，没有节点对象。冲突时看下一格（线性探测），相邻的格子通常在同一条缓存行里，所以比链表快。
- **哈希函数用乘法，取高位**：`(key * 0x9E3779B97F4A7C15) >>> shift`，其中 `shift = 64 - log2(容量)`。这个常数是 2⁶⁴ 除以黄金比例。乘法让 key 的每一位都影响乘积的高位，取高位就拿到混合得最好的几位。如果写成 `key & (容量 - 1)`，只有最低几位起作用，而 ticker 的低位是最后一两个字符，很容易大量冲突；测试里低 32 位全为 0 的 key 会全部落进同一格。
- **容量是 2 的幂**：向后走一格写成 `(i + 1) & (容量 - 1)`，不用取余。
- **装载因子不超过 3/4，保证表里永远有空格**：`get` 靠「碰到空格就停」结束；表装满了，查不存在的 key 会无限循环。线性探测的期望探测次数（Knuth 公式）在装载因子 α 时，查找成功约 (1 + 1/(1−α))/2，查找失败约 (1 + 1/(1−α)²)/2；α = 0.75 时分别是 2.5 和 8.5。
- **扩容要重新插入**：容量变了，`shift` 变了，每个 key 的格子都变了，不能把旧数组原样复制过去。重新插入时调用 `put`，此时装载因子只有 3/8，不会再触发扩容。
- 每个槽位 16 字节（key 8 + value 8），装载因子在 3/8 到 3/4 之间，所以每个条目约 21 到 43 字节。

**Java**

```java
private long[] keys = new long[16], vals = new long[16];  // key 0 表示空格
private int size, shift = 60;                             // shift = 64 - log2(容量)

private int slot(long key) { return (int) ((key * 0x9E3779B97F4A7C15L) >>> shift); }

public void put(long key, long value) {
    if (key <= 0) throw new IllegalArgumentException("key must be > 0: " + key);
    if ((size + 1) * 4 > keys.length * 3) grow();
    int i = slot(key);
    while (keys[i] != 0 && keys[i] != key) i = (i + 1) & (keys.length - 1);
    if (keys[i] == 0) { keys[i] = key; size++; }
    vals[i] = value;
}

public OptionalLong get(long key) {
    for (int i = slot(key); keys[i] != 0; i = (i + 1) & (keys.length - 1))
        if (keys[i] == key) return OptionalLong.of(vals[i]);
    return OptionalLong.empty();
}

private void grow() {
    long[] oldKeys = keys, oldVals = vals;
    keys = new long[oldKeys.length * 2];
    vals = new long[oldKeys.length * 2];
    shift--;
    size = 0;
    for (int i = 0; i < oldKeys.length; i++) if (oldKeys[i] != 0) put(oldKeys[i], oldVals[i]);
}
```

（`size()` 返回 `size`，`capacity()` 返回 `keys.length`。）

**C++**

```cpp
std::vector<std::uint64_t> keys_ = std::vector<std::uint64_t>(16);  // key 0 表示空格
std::vector<std::int64_t> vals_ = std::vector<std::int64_t>(16);
std::size_t size_ = 0;
int shift_ = 60;  // 64 - log2(容量)

std::size_t slot(std::uint64_t key) const { return (key * 0x9E3779B97F4A7C15ULL) >> shift_; }

void put(std::uint64_t key, std::int64_t value) {
    if (key == 0) throw std::invalid_argument("key must be > 0");
    if ((size_ + 1) * 4 > keys_.size() * 3) grow();
    std::size_t i = slot(key);
    while (keys_[i] != 0 && keys_[i] != key) i = (i + 1) & (keys_.size() - 1);
    if (keys_[i] == 0) { keys_[i] = key; ++size_; }
    vals_[i] = value;
}

std::optional<std::int64_t> get(std::uint64_t key) const {
    for (std::size_t i = slot(key); keys_[i] != 0; i = (i + 1) & (keys_.size() - 1))
        if (keys_[i] == key) return vals_[i];
    return std::nullopt;
}

void grow() {
    auto old_keys = std::move(keys_);
    auto old_vals = std::move(vals_);
    keys_.assign(old_keys.size() * 2, 0);
    vals_.assign(old_keys.size() * 2, 0);
    --shift_;
    size_ = 0;
    for (std::size_t i = 0; i < old_keys.size(); ++i)
        if (old_keys[i] != 0) put(old_keys[i], old_vals[i]);
}
```

复杂度：`put` / `get` 平均 O(1)；`grow` 是 O(容量)，但每次容量翻倍，均摊到每次 `put` 仍是 O(1)。

## Part 3 · 口头追问和回答

**1. 为什么整数 key 比字符串 key 快？**

三个原因。第一，比较：整数一条指令，字符串要先跟指针找到数据，再逐字节比较。第二，哈希：整数一次乘法，字符串要扫一遍所有字符。第三，内存：整数直接存在数组里，字符串 key 要另外分配对象，每次查找多一次指针追逐（pointer chasing），多一次可能的缓存未命中。Java 里 `HashMap<String, Long>` 的每个条目背后还有 `Node`、`String`、`byte[]`、`Long` 四个对象。

**2. 要支持删除怎么办？为什么不能直接把格子清空？**

线性探测的查找靠「碰到空格就停」。如果 A 和 B 的家是同一格，B 因为 A 占着被挤到下一格；删掉 A 并清空，再查 B 时，从家出发第一格就是空，会误判成不存在。两种办法：一是墓碑（tombstone）：被删的格子标成「已删除」，`get` 继续往后找，`put` 可以复用；墓碑多了要在扩容或定期重建时清掉，装载因子要把墓碑也算进去。二是反向移位删除（backward shift deletion）：删除后把探测链后面本该往前挪的 key 往前搬，不留墓碑，但代码更复杂。

**3. 为什么装载因子取 3/4，不让表装满？**

线性探测会聚集（clustering）：冲突的 key 连成一片，越长越容易被新 key 撞上。期望探测次数随装载因子急剧上升：按 Knuth 公式，α = 0.75 时失败查找约 8.5 次，α = 0.9 时约 50.5 次。装满则查不存在的 key 会无限循环。3/4 是用内存换速度的折中。

**4. 开盘前就知道全部 ticker，还能怎么优化？**

用完美哈希（perfect hashing）：key 集合固定时，可以在开盘前搜索一个哈希函数（或一组参数），让所有 ticker 映射到互不相同的格子，最小完美哈希还能让格子数恰好等于 ticker 数。之后查找没有冲突，不用探测，value 放进一个长度恰好为 n 的数组。要注意：完美哈希只保证集合内的 key 不冲突，集合外的 key 也会被映射到某一格，所以查找时仍要比较一次 key。另一个实用做法：行情订阅时把 ticker 解析成下标缓存起来，之后每条消息直接用下标，连哈希都省了。

**5. 缓存行对这张表的布局有什么影响？**

CPU 一次从内存读一整条缓存行，常见是 64 字节。key 和 value 分成两个数组，一次查找要碰两条缓存行（可能两次未命中）；把 key 和 value 交错放在同一个数组里，16 字节一个槽位，一条缓存行放 4 个槽位，命中后 value 就在旁边，线性探测的下几格也大概率在同一行里。代价是纯扫描 key 时多读了 value。实际选哪种要测量，不能凭感觉。

**6. `std::hash<uint64_t>` 在常见实现里是恒等函数，这意味着什么？**

在 libstdc++ 和 libc++ 里，整数的 `std::hash` 就是把整数本身当哈希值。libstdc++ 的桶数是质数，对质数取余能把 key 散开，所以恒等哈希还能用；但自己写的 2 的幂容量加掩码的表，直接用恒等哈希就会让低位相同的 key 全部冲突。结论：2 的幂容量的表必须自己加一步混合，例如乘法哈希取高位。

## 常见错误

1. 哈希函数写成 `key & (容量 - 1)`：低位相同的 key 全部挤进同一格，查找退化成线性扫描。
2. 扩容时把旧数组原样复制：容量变了，每个 key 的格子都变了，必须逐个重新插入。
3. 让装载因子达到 100%：查不存在的 key 找不到空格，无限循环。
4. 把 0 当合法 key，又用 0 当空格标记：写入的 key 会被当成空格，找不到。
5. `decode` 不检查每个字节：任意 `long` 都能「解码」出乱码，或者在字节中间的 0 处悄悄截断。
6. 删除时直接把格子清空：探测链被截断，后面的 key 查不到。
