---
id: hl-oa01-comparator-reversed
node: problems.oa01-job-chain
type: qa
step: 9
---
## Q
Java 里怎样写「按总时长降序、相同时按起始 job 升序」的 `Comparator`？`reversed()` 放错位置会怎样？

## A
```java
out.sort(Comparator.comparingLong(Chain::totalSeconds).reversed()
                   .thenComparingInt(Chain::startJob));
```
从左往右读：按 `totalSeconds` 比较 → 整体反过来（降序）→ 相等时按 `startJob` 升序。`Chain::totalSeconds` 是方法引用，等价于 `c -> c.totalSeconds()`。

经典坑：`comparingLong(A).thenComparingInt(B).reversed()` 把**两个**条件都反过来，起始 job 变成降序。`reversed()` 要紧跟在要反转的那个比较器后面。

题面没规定相同时长的 tie-break 时，自己选一个（这里是 `start_job` 升序）并说出口，是好习惯。另一个变式：按 job 数升序、相同按总时长降序 → `comparingInt(Chain::count).thenComparing(Comparator.comparingLong(Chain::totalSeconds).reversed())`。
