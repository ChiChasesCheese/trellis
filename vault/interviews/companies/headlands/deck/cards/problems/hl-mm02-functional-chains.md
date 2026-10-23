---
id: hl-mm02-functional-chains
node: problems.mm02-job-runner
type: qa
step: 7
---
## Q
全函数式写法（`Functional.java`）怎么做 `chains`？`Stream.iterate`、`teeing` 的用法和限制是什么？

## A
```java
Map<Long, Long> predecessors = jobs.values().stream()
    .map(Job::next).filter(next -> next != 0)
    .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));   // 每个 job 有几个前驱
if (!jobs.keySet().containsAll(predecessors.keySet())) throw ...;                  // 每个 next 都必须存在
if (predecessors.values().stream().anyMatch(count -> count > 1)) throw ...;        // 汇合 / ρ 字形
List<Chain> chains = jobs.values().stream()
    .filter(job -> !predecessors.containsKey(job.id()))                            // 起点 = 没有前驱的 job
    .map(start -> walk(start, jobs))
    .sorted(LONGEST_FIRST)
    .toList();
if (chains.stream().mapToLong(Chain::jobs).sum() != jobs.size()) throw ...;        // 环

private static Chain walk(Job start, Map<Long, Job> jobs) {
    return Stream.iterate(start, Objects::nonNull, job -> jobs.get(job.next()))     // Java 9 带结束条件的 iterate
        .collect(Collectors.teeing(                                                // Java 12：同一个流喂两个收集器
            Collectors.reducing((earlier, later) -> later),                        // 最后一个元素，Optional<Job>
            Collectors.summarizingLong(Job::runtime),                              // 一次遍历得个数和总和
            (last, stats) -> new Chain(start.id(), last.orElseThrow().id(),
                    Math.toIntExact(stats.getCount()), stats.getSum())));
}
```
要点：
- **受检异常不要放进 lambda**：`Function/Predicate` 签名不允许抛受检异常，所以三道校验写在流**外面**的普通 `if`，流只做纯计算；
- `Stream.iterate` 能结束靠 `jobs.get(0)` 返回 `null`，这依赖 `parse` 已拒绝 id 为 0 的 job——**隐含耦合**，注释写明；next 指向不存在的 job 也得到 `null` 悄悄结束，看起来像正常链尾，所以 `containsAll` 检查必须放在 `walk` **之前**（错误版本「missing next not checked」）；
- 能结束的另一个前提和命令式一样：「前驱 ≤ 1」必须先检查，否则 ρ 字形让 `iterate` 变无限流，`collect` 永不返回（错误版本「two predecessors allowed」被 5 秒超时判失败）；
- `groupingBy(..., counting())` 比命令式 `Set.add` 多知道每个 job 有**几个**前驱，代价是每个 job 装箱一个 `Long`；
- 比较器提成常量 `LONGEST_FIRST` 读起来就是一句话。

**两种写法怎么选**（5 万条短链 / 1 条 10 万 job 长链，取最快）：命令式 754 / 243 ms，函数式 711 / 329 ms，同一量级，看可读性。函数式把校验分成清楚的几段，命令式一次循环做多件事、更好逐行跟踪。面试时**两种都可以，不要为了显得高级而用**；`teeing`、`reducing` 若团队没人熟悉反而扣分。两者共同风险，必须在注释说清：**为什么这个循环一定会结束**。
