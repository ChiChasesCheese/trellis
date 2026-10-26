# oa01 · 解法与原理

这一题不考算法技巧，考的是把含糊的题面变成一份完整的校验清单，并把输出格式做得一字不差。下面先说开场 3 分钟怎么做，然后 Part 1 写出合法输入的主流程，Part 2 补上校验，之后是怎么在 2 分钟里讲清你的 OA 解法，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "Each row says which job runs next, so the input is a set of singly linked lists. I'll index rows by id, find each chain's head, which is a job nobody points to, and walk it. Before I start: what order should the chains be printed in, how is the average rounded, and does one bad row make the whole output `Malformed Input`?"

面试官通常会说：按总时长从大到小、相同时起点编号小的在前；平均值截断成整秒；一行不对就整个输出 `Malformed Input`。

## Part 1 · 合法输入：建表，从链头往下走

**思路**：逐行读入，跳过表头和空行，把每个任务存进三张表：`next[id]`（下一个任务）、`time[id]`（运行时间）、`prev[next]`（谁指向它）。没有出现在 `prev` 里的任务就是链头。从每个链头顺着 `next` 走，走一步数一个、加一次时间，走到 `next = 0` 为止。最后排序、输出。

**原理**：每行只有一个 `next`，所以「谁是下一个」是一个查表动作；链头就是入度（被多少个任务指向）为 0 的任务。有了 `prev` 表，找链头不需要再扫一遍。Java 用 `LinkedHashMap` 放 `next`，遍历顺序等于输入顺序，输出稳定。

排序规则 `a[3] != b[3] ? 总时长降序 : 起点升序` 里，比较器用 `Long.compare(b, a)` 而不是 `b - a`，因为减法在差很大时会溢出。

**Java**

```java
    public static List<String> solve(List<String> lines) {
        Map<Integer, Integer> next = new LinkedHashMap<>(), prev = new HashMap<>();
        Map<Integer, Long> time = new HashMap<>();
        for (String raw : lines) {
            String line = raw.strip();
            if (line.isEmpty() || line.startsWith("#")) continue;
            String[] f = line.split(",");
            int id = Integer.parseInt(f[0].strip()), nx = Integer.parseInt(f[2].strip());
            next.put(id, nx);
            time.put(id, Long.parseLong(f[1].strip()));
            if (nx != 0) prev.put(nx, id);
        }
        List<long[]> chains = new ArrayList<>();
        for (int head : next.keySet()) {
            if (prev.containsKey(head)) continue;
            long total = 0;
            int count = 0, last = head;
            for (int cur = head; cur != 0; cur = next.get(cur)) { total += time.get(cur); count++; last = cur; }
            chains.add(new long[] {head, last, count, total});
        }
        chains.sort((a, b) -> a[3] != b[3] ? Long.compare(b[3], a[3]) : Long.compare(a[0], b[0]));
        List<String> out = new ArrayList<>(List.of("-"));
        for (long[] c : chains) {
            out.addAll(List.of("start_job: " + c[0], "last_job: " + c[1], "number_of_jobs: " + c[2],
                    "job_chain_runtime: " + hhmmss(c[3]), "average_job_time: " + hhmmss(c[3] / c[2]), "-"));
        }
        return out;
    }
```

**C++**

```cpp
inline std::vector<std::string> solve(const std::vector<std::string>& lines) {
    std::unordered_map<int, int> next, prev;
    std::unordered_map<int, long long> time;
    std::vector<int> order;  // job ids in input order
    for (const std::string& raw : lines) {
        std::string_view line = trim(raw);
        if (line.empty() || line[0] == '#') continue;
        auto f = split(line);
        int id = std::stoi(std::string(f[0])), nx = std::stoi(std::string(f[2]));
        next[id] = nx; time[id] = std::stoll(std::string(f[1])); order.push_back(id);
        if (nx != 0) prev[nx] = id;
    }
    struct Chain { int head, last, count; long long total; };
    std::vector<Chain> chains;
    for (int head : order) {
        if (prev.count(head)) continue;
        Chain c{head, head, 0, 0};
        for (int cur = head; cur != 0; cur = next[cur]) { c.total += time[cur]; c.count++; c.last = cur; }
        chains.push_back(c);
    }
    std::sort(chains.begin(), chains.end(), [](const Chain& a, const Chain& b) {
        return a.total != b.total ? a.total > b.total : a.head < b.head;
    });
    std::vector<std::string> out{"-"};
    for (const Chain& c : chains) {
        out.insert(out.end(), {"start_job: " + std::to_string(c.head), "last_job: " + std::to_string(c.last),
                               "number_of_jobs: " + std::to_string(c.count), "job_chain_runtime: " + hhmmss(c.total),
                               "average_job_time: " + hhmmss(c.total / c.count), "-"});
    }
    return out;
}
```

复杂度：读入 O(n)，每个任务只被走一次 O(n)，排序 O(k log k)（k 是链的条数，k <= n）。空间 O(n)。

## Part 2 · 校验

**思路**：把「不合法」拆成两层来查。

1. **读每一行的时候**：字段数必须正好是 3（`split(",", -1)` 的 `-1` 保留末尾的空字段，所以 `1,2,0,` 会被抓到）；三个字段都必须是整数且放得进类型（Java 的 `parseInt` / `parseLong` 抛 `NumberFormatException`，C++ 用 `from_chars` 并检查它有没有读完整个字段）；`job_id > 0`；`run_time >= 0`；`next_job_id >= 0`；`job_id` 不能重复。
2. **读完所有行以后**：`next_job_id` 必须指向一个存在的任务；一个任务不能被两个任务指向（`prev.put` 返回了旧值，或者 `emplace` 没插进去）；最后检查有没有环。

**原理：为什么「数一数走到了多少个任务」就能查出环**

先通过第 2 层的前两项检查，保证每个任务的入度 <= 1，并且每个 `next` 都指向存在的任务。

- 因为入度 <= 1，两条链不可能在中间汇合，所以每个任务最多被走到一次。
- 任务 X 没被任何链头走到，就沿着「谁指向我」一直往回找。每个任务只有一个前驱，所以这条路径唯一。路径不可能停在某个链头上（否则那个链头会走到 X），任务又是有限的，所以路径一定绕回自己：X 在一个环上。
- 所以把每条链的长度加起来，等于任务总数就没有环，少了就一定有环。一次比较，不需要染色的深度优先搜索。

指向自己的任务（`4,1,4`）也在同一个检查里被抓到：它的 `prev` 是自己，所以它不是链头，没有任何链头走到它。

Java 版把读入、`prev` 检查和环检查依次排开；`next.get(cur)` 在 `cur` 不存在时本来会返回 `null`，但前面的检查已经排除了悬空的 `next`。

**Java**

```java
    public static List<String> solve(List<String> lines) {
        List<String> malformed = List.of("Malformed Input");
        Map<Integer, Integer> next = new LinkedHashMap<>(), prev = new HashMap<>();
        Map<Integer, Long> time = new HashMap<>();
        try {
            for (String raw : lines) {
                String line = raw.strip();
                if (line.isEmpty() || line.startsWith("#")) continue;
                String[] f = line.split(",", -1);
                if (f.length != 3) return malformed;
                int id = Integer.parseInt(f[0].strip()), nx = Integer.parseInt(f[2].strip());
                long t = Long.parseLong(f[1].strip());
                if (id <= 0 || t < 0 || nx < 0 || next.containsKey(id)) return malformed;
                next.put(id, nx);
                time.put(id, t);
            }
        } catch (NumberFormatException e) {
            return malformed;
        }
        for (var e : next.entrySet()) {
            int nx = e.getValue();
            if (nx == 0) continue;
            if (!next.containsKey(nx) || prev.put(nx, e.getKey()) != null) return malformed;  // 悬空 / 两个前驱
        }
        List<long[]> chains = new ArrayList<>();
        int seen = 0;
        for (int head : next.keySet()) {
            if (prev.containsKey(head)) continue;
            long total = 0;
            int count = 0, last = head;
            for (int cur = head; cur != 0; cur = next.get(cur)) { total += time.get(cur); count++; last = cur; }
            seen += count;
            chains.add(new long[] {head, last, count, total});
        }
        if (seen != next.size()) return malformed;  // 没被任何链头走到的 job 都在环上
        chains.sort((a, b) -> a[3] != b[3] ? Long.compare(b[3], a[3]) : Long.compare(a[0], b[0]));
        List<String> out = new ArrayList<>(List.of("-"));
        for (long[] c : chains) {
            out.addAll(List.of("start_job: " + c[0], "last_job: " + c[1], "number_of_jobs: " + c[2],
                    "job_chain_runtime: " + hhmmss(c[3]), "average_job_time: " + hhmmss(c[3] / c[2]), "-"));
        }
        return out;
    }
```

**C++**

```cpp
/// The whole token must be an integer that fits long long (from_chars reports "stopped early" and "out of range").
inline bool to_num(std::string_view s, long long& v) {
    s = trim(s);
    auto [p, ec] = std::from_chars(s.data(), s.data() + s.size(), v);
    return ec == std::errc{} && p == s.data() + s.size();
}

inline std::vector<std::string> solve(const std::vector<std::string>& lines) {
    const std::vector<std::string> bad{"Malformed Input"};
    std::unordered_map<int, int> next, prev;
    std::unordered_map<int, long long> time;
    std::vector<int> order;  // job ids in input order
    for (const std::string& raw : lines) {
        std::string_view line = trim(raw);
        if (line.empty() || line[0] == '#') continue;
        auto f = split(line);
        long long id, t, nx;
        if (f.size() != 3 || !to_num(f[0], id) || !to_num(f[1], t) || !to_num(f[2], nx)) return bad;
        if (id <= 0 || id > INT_MAX || t < 0 || nx < 0 || nx > INT_MAX || next.count(id)) return bad;
        next[id] = nx; time[id] = t; order.push_back(id);
    }
    for (int id : order) {
        int nx = next[id];
        if (nx != 0 && (!next.count(nx) || !prev.emplace(nx, id).second)) return bad;  // unknown next / two parents
    }
    struct Chain { int head, last, count; long long total; };
    std::vector<Chain> chains;
    std::size_t seen = 0;
    for (int head : order) {
        if (prev.count(head)) continue;
        Chain c{head, head, 0, 0};
        for (int cur = head; cur != 0; cur = next[cur]) { c.total += time[cur]; c.count++; c.last = cur; }
        seen += c.count;
        chains.push_back(c);
    }
    if (seen != order.size()) return bad;  // jobs no head walks to are on a cycle
    std::sort(chains.begin(), chains.end(), [](const Chain& a, const Chain& b) {
        return a.total != b.total ? a.total > b.total : a.head < b.head;
    });
    std::vector<std::string> out{"-"};
    for (const Chain& c : chains) {
        out.insert(out.end(), {"start_job: " + std::to_string(c.head), "last_job: " + std::to_string(c.last),
                               "number_of_jobs: " + std::to_string(c.count), "job_chain_runtime: " + hhmmss(c.total),
                               "average_job_time: " + hhmmss(c.total / c.count), "-"});
    }
    return out;
}
```

复杂度：和 Part 1 一样，O(n + k log k)。

## 怎么在 2 分钟里讲你的 OA 解法

面试官可能会问：「你当时的 OA 是怎么做的？」你可以按下面四步说，每一步一两句话。

1. **题意**：日志的每一行是一个任务和它的下一个任务，所以整份输入是若干条单链表。
2. **数据结构**：把每一行存进哈希表，`next` 表示下一个任务，另一张表记录谁指向它。没有人指向的任务就是链头。
3. **主流程**：从每个链头顺着 `next` 走到 `next = 0`，边走边数任务数、累加运行时间，得到起点、终点、数量、总时长，平均值用整数除法截断。然后按总时长降序、起点升序排序输出，时间格式化成 `hh:mm:ss`，分钟和秒要对 60 取余。
4. **校验**：我把所有不合法的情形列成清单：格式不对、数值越界、编号重复、`next` 指向不存在的任务、一个任务有两个前驱、有环。前五类在读入时查出来；环靠「所有链头走到的任务数加起来必须等于任务总数」判断。整个过程每个任务只处理常数次，是 O(n)。

可以补一句：「如果输入有任何一行不对，我就只输出 `Malformed Input`，不输出部分结果。」

## Part 3 · 口头追问和回答

**1. 为什么「走完所有链头之后，还有任务没被走到」就一定说明有环？**

见 Part 2 的原理。前提是已经保证每个任务入度 <= 1 且 `next` 都存在：这时两条链不会汇合，没被走到的任务只能沿着唯一的前驱一路往回，回不到链头，只能绕成一个环。

**2. 复杂度是多少？输出前的排序占多少？**

读入、建表、走链都是 O(n)，每个任务只被访问常数次。排序只对链排，k 条链花 O(k log k)，k 不会超过 n。最坏情况是每个任务自成一条链（k = n），这时排序是 O(n log n) 并且主导整个运行时间；通常链很长，k 很小，排序可以忽略。

**3. 一条链有一百万个任务，递归地走链会怎样？**

会栈溢出：每走一步递归就占一个栈帧，栈的大小是固定的。上面的写法是 `for` 循环，栈空间是 O(1)，一百万个任务没有问题。这也是为什么走链要写成循环，不写成递归。

**4. 文件大到内存放不下，怎么办？能边读边输出吗？**

不能边读边输出：任何一行不对，整个输出就只是 `Malformed Input`，所以读完全部输入才能决定输出什么。可以做的是减少内存：只保存每个任务的 `next`、运行时间和是否被指向，而不是整行字符串；任务编号如果能放进 `int`，用 `int` 数组和紧凑的哈希表。真的放不下时，先按 `job_id` 做外部排序，再顺序扫描做校验和走链；这时每次「走到下一个」变成一次查找，要用有序文件加二分，或者分块处理。面试里点到这个思路就够了。

**5. 一条链的总时长加起来超出 `long` 的范围怎么办？**

单个任务的运行时间是 `long`，几个接近 9.2 × 10^18 的任务加起来就会溢出。Java 里可以用 `Math.addExact` 检测，溢出就当作 `Malformed Input` 或者改用 `BigInteger`；C++ 里有符号溢出是未定义行为，要用 `__builtin_add_overflow`。要先问面试官运行时间的上限，通常题目会保证不会发生，这时就不用处理。

**6. 任务编号很稀疏、很大，用数组代替哈希表可以吗？**

不行。数组的大小取决于最大的编号，编号接近 20 亿时数组要占几个 GB，而任务可能只有几行。哈希表的空间只跟任务个数有关，平均每次查找 O(1)。如果编号是 1 到 n 的紧凑整数，数组更快也更省空间，可以在面试里说出这个条件。

## 常见错误

1. 分钟没有对 60 取余：7200 秒输出成 `02:120:00`。
2. 平均值用浮点数除再四舍五入：35 / 2 = 17.5 会变成 18，题目要的是截断后的 17。
3. 只从 `next = 0` 的任务往回找：环上没有这样的任务，`1,10,0` + `2,10,3` + `3,10,2` 会被当作合法输入。
4. 两个任务指向同一个 `next` 时，只取第一个：分叉被悄悄忽略，应该是 `Malformed Input`。
5. 遇到坏行时抛出异常而不是返回 `Malformed Input`，或者已经输出了前几条链再发现坏行：整个输出只能有这一行。
6. 用 `split(",")` 解析：它会丢掉末尾的空字段，`1,2,0,` 被当成三个字段而通过。要用 `split(",", -1)`，把字段数卡在正好 3。
7. 以为 Java 和 C++ 的数字解析一样严格：Java 的 `Integer.parseInt("+5")` 返回 5，C++ 的 `std::from_chars` 遇到 `+` 直接失败。题目没说 `+5` 合不合法时，先问清楚；要和 C++ 一致，就在 Java 里先检查第一个字符是数字或 `-`。
