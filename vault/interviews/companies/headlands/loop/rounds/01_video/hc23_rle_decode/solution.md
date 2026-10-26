# hc23 · 解法与原理

解码本身是一个只有两个状态变量的扫描：当前攒出来的 count，和「是否已经看到过数字」。流式版就是把这两个局部变量变成对象的字段。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll scan left to right, accumulating digits into a count, and when I see a non-digit I append that character `count` times. Before I start: can the value be a space or punctuation? Is a leading zero like `03a` allowed? And on invalid input, should I throw?"

面试官通常会说：值是任意非数字字符，非法输入抛异常。问出「值不是数字」这一点很关键：它让解析没有歧义，遇到数字就是 count 的一部分，遇到非数字就是值。

## Part 1 · 一次性解码

**思路**：用 `count` 和 `hasCount` 两个变量。遇到数字：`count = count * 10 + 数字`，并标记 `hasCount`。遇到非数字：先检查 `hasCount` 且 `count > 0`，再把这个字符追加 `count` 次，然后把两个变量清零。扫完以后，如果 `hasCount` 还是真，说明末尾有多余的数字。

**原理：为什么要两个变量，而不是只看 `count == 0`**

`count == 0` 有两种成因：根本没有数字（`"a"`），或者数字本身是 0（`"0a"`）。两种都非法，但只靠 `count` 时，「还没看到数字」和「看到了一个 0」分不开。末尾检查更明显：`"3a0"` 扫完 `count` 是 0，`"3a"` 扫完 `count` 也是 0，一个非法一个合法，只有 `hasCount` 能区分它们。

**Java**

```java
public static String decode(String encoded) {
    var out = new StringBuilder();
    int count = 0;
    boolean hasCount = false;
    for (char c : encoded.toCharArray()) {
        if (c >= '0' && c <= '9') {
            count = count * 10 + (c - '0');
            hasCount = true;
        } else {
            if (!hasCount || count == 0) throw new IllegalArgumentException("bad count before '" + c + "'");
            out.append(String.valueOf(c).repeat(count));
            count = 0;
            hasCount = false;
        }
    }
    if (hasCount) throw new IllegalArgumentException("count without a value at the end");
    return out.toString();
}
```

**C++**

```cpp
static std::string decode(const std::string& encoded) {
    std::string out;
    int count = 0;
    bool has_count = false;
    for (const char c : encoded) {
        if (c >= '0' && c <= '9') {
            count = count * 10 + (c - '0');
            has_count = true;
        } else {
            if (!has_count || count == 0) throw std::invalid_argument("bad count before a value");
            out.append(static_cast<std::size_t>(count), c);
            count = 0;
            has_count = false;
        }
    }
    if (has_count) throw std::invalid_argument("count without a value at the end");
    return out;
}
```

判断数字用 `c >= '0' && c <= '9'`，不用 Java 的 `Character.isDigit`：它对全角数字这类其他文字的数字也返回真，接着算 `c - '0'` 就会得到一个很大的错误计数。

复杂度：时间 O(n + 输出长度)，额外空间只有两个变量和输出本身。

## Part 2 · 流式解码

**思路**：把 `count` 和 `hasCount` 从局部变量改成字段。`feed` 里的循环和 Part 1 完全一样，只是每次处理一块，返回这一块新追加的文本。再加一个 `finish()`：如果 `hasCount` 还为真，抛异常。

**原理：为什么数字不能马上输出**

看到 `1` 的时候，你不知道后面是字符还是另一个数字：`"1a"` 是一个 a，`"10a"` 是十个 a。所以数字只能攒着，等到非数字字符到达才能确定 count。这就是为什么对象要保存状态，也是 `"3a2"` 之后 `feed("b1")` 才能输出 `"bb"` 的原因：上一块留下的 `2` 接上了这一块的 `b`。

**为什么需要 `finish()`**：`feed` 看不到「输入结束」。`feed("3a2")` 之后，`2` 可能还会被后续的 `0` 续成 20，所以此时不能报错；只有调用方说「没有更多输入了」，才能判断末尾的数字是不是多余的。

缺 count 和 count 为 0 是在字符到达时才能判定的（`feed("3")` 然后 `feed("a0")` 里的 `0` 要等到下一个字符才知道是 0），所以这两种错误在字符所在的那次 `feed` 报出。

**Java**

```java
private int count;
private boolean hasCount;

public String feed(String chunk) {
    var out = new StringBuilder();
    for (char c : chunk.toCharArray()) {
        if (c >= '0' && c <= '9') {
            count = count * 10 + (c - '0');
            hasCount = true;
        } else {
            if (!hasCount || count == 0) throw new IllegalArgumentException("bad count before '" + c + "'");
            out.append(String.valueOf(c).repeat(count));
            count = 0;
            hasCount = false;
        }
    }
    return out.toString();
}

public void finish() {
    if (hasCount) throw new IllegalArgumentException("count without a value at the end");
}
```

**C++**

```cpp
std::string feed(const std::string& chunk) {
    std::string out;
    for (const char c : chunk) {
        if (c >= '0' && c <= '9') {
            count_ = count_ * 10 + (c - '0');
            has_count_ = true;
        } else {
            if (!has_count_ || count_ == 0) throw std::invalid_argument("bad count before a value");
            out.append(static_cast<std::size_t>(count_), c);
            count_ = 0;
            has_count_ = false;
        }
    }
    return out;
}

void finish() {
    if (has_count_) throw std::invalid_argument("count without a value at the end");
}
// members: int count_ = 0; bool has_count_ = false;
```

复杂度：每块 O(块长 + 这一块解出的文本长度)；对象本身只存一个整数和一个标记。

## Part 3 · 口头追问和回答

**1. count 很大怎么办？比如 `"2000000000z"`，或者很多条这样的记录。**

有两层问题。第一层是解析 count：`int` 最大是 2147483647，再多一位（比如 `"9999999999z"`），`count * 10 + digit` 就溢出了。Java 会静默回绕，C++ 是未定义行为（UB）。所以要么用 `long` / `unsigned long long`，并在每一步检查（Java `Math.multiplyExact`，C++ `__builtin_mul_overflow`），超限就报错；要么跟面试官约定 count 的上限。第二层是输出总长：每条记录的 count 都合法，总和也可能溢出，更重要的是不可能放进内存。这时不要真的展开：先累加总长度（同样检查溢出），超过上限就拒绝；或者返回一个惰性的迭代器 / 流，边读边写出去，不在内存里存整串。

**2. 不展开字符串，怎么读第 k 个字符？**

先扫一遍编码，把每条记录解析成 `(count, 值)`，并记下前缀和 `prefix[i] = 前 i 条记录的 count 之和`。要读第 k 个字符（从 0 开始），在 `prefix` 里二分，找到第一个 `prefix[i + 1] > k` 的记录 i，答案就是它的值。预处理 O(n)（n 是记录数），每次查询 O(log n)，额外空间 O(n)，和展开后的字符串有多长无关。`prefix` 要用 64 位，因为总长可能很大；k 超出总长时抛 `std::out_of_range` / `IndexOutOfBoundsException`。

**3. 反过来，怎么编码？**

扫描原文，把连续相同的字符合成一段，输出「这一段的长度 + 字符」。几个要点：长度从 1 开始写（`"a"` 编码成 `"1a"`），因为解码要求 count 为正；这个格式里值不是数字，所以 `"10c"` 不会有歧义——如果原文里允许数字字符，`"1" + "1"` 会编码成 `"111"`，解码时分不清，那就要加转义，或者换成固定宽度的 count。最坏情况是原文里相邻字符全都不同，编码长度是原文的 2 倍（每个字符变成 `"1x"`）。

**4. 流式解码的内存用量是多少？一块输入解出来的文本太大怎么办？**

解码器自己的状态只有一个整数和一个标记，和已经处理了多少输入无关。但 `feed` 返回的文本长度可能远大于块长：块 `"2000000000z"` 只有 11 个字符，却对应 20 亿个字符的输出。所以「内存有界」只对解码器状态成立，对返回值不成立。要真的有界，就别返回字符串：让 `feed` 接受一个输出回调（或者 `Writer` / `ostream`），每解出一小段（比如最多 8 KiB）就交给下游，不在内存里积累。

**5. 为什么 `feed` 不能在看到数字时就输出？为什么需要 `finish()`？**

见 Part 2 的原理：数字没有结束之前，不知道 count 是多少，更不知道配哪个字符。`finish()` 是调用方告诉解码器「不会再有数字接上来」的唯一方式，没有它，末尾的 `"3a2"` 和一条还没到齐的 `"3a2"` 无法区分。

## 常见错误

1. 只用一个 `count` 变量，用 `count == 0` 表示「没有数字」：`"0a"` 和 `"a"` 分不开，或者末尾 `"3a0"` 漏报。
2. 遇到数字就写成 `count = c - '0'`：多位数 `10c` 解成一个 `c`。
3. 一遇到非数字就输出，但忘了把 `count` 清零：下一条记录继承上一条的 count。
4. 流式版把 `count` 留在 `feed` 的局部变量里：count 被切在两块之间时，上一块的数字丢掉。
5. 流式版没有 `finish()`，或者在 `feed` 里看到块末尾的数字就报错：合法的分块 `"3a2"` + `"b"` 被拒绝。
6. 用 `int` 累乘 count 而不检查：count 超过 2147483647 之后静默回绕（Java）或未定义行为（C++）。
