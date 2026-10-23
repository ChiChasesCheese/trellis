---
id: hl-mm02-parse-pitfalls
node: problems.mm02-job-runner
type: qa
step: 5
---
## Q
Job Runner 的解析有哪三个容易踩的坑（`split`、`parseLong`、`putIfAbsent`）？数据类型怎么用 record 表示？

## A
```java
record Job(long id, long runtime, long next) {}
record Chain(long start, long last, int jobs, long runtime) {
    long averageRuntime() { return runtime / jobs; }   // long 整数除法本身就是截断
}
String[] fields = line.strip().split(",", -1);       // 坑 1：-1
if (!NON_NEGATIVE_INTEGER.matcher(field).matches())  // 坑 2：先用正则检查，再 parseLong
if (jobs.putIfAbsent(job.id(), job) != null)         // 坑 3：putIfAbsent 一步判断重复
```
1. **`split(",")` 会丢掉末尾的空字段**：`"1,60,0,".split(",")` 得到 3 个字段，看起来格式正确；加 `-1` 得 4 个字段才会被判格式错误。这个错误版本一开始**没被抓到**，后来补了测试「trailing comma after three fields」。
2. **`Long.parseLong` 接受 `"+5"`**，还会对超出 long 范围的数字抛 `NumberFormatException`。先用正则 `\d+` 把关，再把 `NumberFormatException` 转成自己的异常。
3. **`Map.putIfAbsent`** 在 key 已存在时返回旧值且不覆盖；先 `containsKey` 再 `put` 也行但要查两次表。用 `LinkedHashMap` 保持输入顺序（结果本身不依赖顺序，调试时更好对照）。

record 可以有自己的方法，`averageRuntime()` 放在 `Chain` 里，因为平均值由链的数据算出。用 `long`：id 可能超过 21 亿（测试 `idsLargerThanInt`），一天的总秒数累加也可能很大。

建链和校验（块 C）：
```java
for (Job job : jobs.values()) {                      // 第一遍：检查每条指向
    if (job.next() == 0) continue;
    if (!jobs.containsKey(job.next())) throw ...;    // 指向不存在的 job
    if (!hasPredecessor.add(job.next())) throw ...;  // Set.add 返回 false：已有别的 job 指向它
}
for (Job first : jobs.values()) {                    // 第二遍：从每个起点沿 next 走到 0
    if (hasPredecessor.contains(first.id())) continue;
    ... while (job.next() != 0) { job = jobs.get(job.next()); ... }
}
if (jobsOnChains != jobs.size()) throw ...;          // 有 job 不在任何一条链上 → 有环
```
- **起点**是没有任何 job 指向的那个 job，不是文件里的第一行（测试 `chainStartIsTheJobNobodyPointsToNotTheFirstLine`）；
- 用**循环不用递归**：一条 10 万 job 的链递归遍历会 `StackOverflowError`（测试 `longChainListedBackwards`）；
- 去掉「两个 job 指向同一个 job」检查后，「two jobs before the same job」仍通过（被环检测顺带抓到），但再加一个自指 job 4，误差正好抵消。
