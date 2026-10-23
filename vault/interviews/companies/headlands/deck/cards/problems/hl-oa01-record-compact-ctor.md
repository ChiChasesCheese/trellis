---
id: hl-oa01-record-compact-ctor
node: problems.oa01-job-chain
type: qa
step: 10
---
## Q
Java 的 record 紧凑构造器（compact constructor）如何用来表示一行 job 并校验单行规则？

## A
```java
public record Job(int id, long runtimeSeconds, int nextId) {
    public Job {
        if (id <= 0) throw new MalformedInputException("job_id must be positive: " + id);
        if (runtimeSeconds < 0) throw new MalformedInputException("negative runtime");
        if (nextId < 0) throw new MalformedInputException("negative next_job_id");
        if (nextId == id) throw new MalformedInputException("self loop: " + id);
    }
}
```
- 一行声明三个 `private final` 字段、构造器、`id()` 等读取方法，以及按字段比较的 `equals` / `hashCode` / `toString`（老写法约 40 行）。
- `public Job { ... }` 没有参数列表，在字段赋值**之前**运行。校验放这里，非法的 `Job` 就构造不出来（**让非法状态无法表示**）。
- 单行规则放构造器，跨行规则（重复、悬空、分叉、环）放 `chains()`。
- 好处：测试可以直接比较 `List<Chain>`。不适用：需要可变字段、需要继承别的类（record 隐式继承 `Record`）。
