---
id: hl-oa01-cpp-parse-and-types
node: problems.oa01-job-chain
type: qa
step: 16
---
## Q
任务链报表的 C++20 版里，整数解析和结果类型各用什么？和 Java 版怎么对应？

## A
- **解析用 `std::from_chars`，不用 `stoi`**：`stoi("12abc")` 返回 12、`stoi(" 7")` 返回 7、`stoi("+5")` 返回 5，都在第一个非法字符处静默停下；`atoi` 连错误都不报告。`from_chars` 不跳空格、不接受 `+`、越界返回 `result_out_of_range`，并通过返回指针告诉你停在哪，要检查 `ptr == 末尾`。
- **结果类型用 `std::variant<Ok, Malformed>` + `std::visit(overloaded{...})`**，等价于 Java 的 sealed + switch：少写一个分支编译不过。
- **`Job` 是聚合体（aggregate）**，可被手工造成 `Job{0, 5, 0}`，所以 `chains()` 里要再调一次 `validate`；Java 的 record 紧凑构造器则让非法对象造不出来。
- **字符串切片**用 `string_view`（零拷贝借用，要保证底层字符串活得更久）。
- 链上累加溢出：有符号溢出是**未定义行为**，用 `__builtin_add_overflow`（Java 用 `Math.addExact`）；总时长超 64 位判为 Malformed，这是必须说出口的假设。
- 集合：`unordered_map<int, size_t>` 存下标；标志位数组用 `vector<char>`，不用位压缩的 `vector<bool>`。
