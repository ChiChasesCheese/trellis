---
id: hl-hc04-versioned-code
node: problems.hc04-queue-mean-snapshot
type: qa
step: 11
---
## Q
`VersionedQueue` 的 `push`、`pop`、`correct` 怎么实现？手跑 push 1、2、3，pop，再 push 9。

## A
```java
public int push(int version, long x) {
    check(version);
    int node = newNode(vTail[version], x);
    var sum = new I128(vHi[version], vLo[version]).plus(x);
    return newVersion(node, vHeadDepth[version], sum);
}
public int pop(int version) {
    check(version);
    if (size(version) == 0) throw new NoSuchElementException(...);
    int h = vHeadDepth[version] + 1;
    long front = val[levelAncestor(vTail[version], h)];
    var sum = new I128(vHi[version], vLo[version]).minus(front);
    return newVersion(vTail[version], h, sum);
}
```
- 旧版本永不改变；版本号按创建顺序从 1 递增；`correct(contents)` 从根连续 `newNode` 产生**独立的链**，`headDepth = 0`，不依赖旧版本，不影响旧历史。
- `check(version)`：未知版本号抛 `IllegalArgumentException` 而非数组越界，区分调用者错误和程序 bug。
- `mean(version)` 在空版本抛 `NoSuchElementException`。

手跑：push 1、2、3 → v3（tail=节点 3，headDepth=0，sum=6，`[1,2,3]`）；`pop(v3)` → v4（headDepth=1，sum=5，`[2,3]`）；`push(v4, 9)` → v5（新节点 9，父亲是节点 3，headDepth=1，sum=14，`[2,3,9]`）。

复杂度：push/mean/size O(1)，pop O(log n)；每节点 4 个原始槽，每版本 4 个。2 万版本：复制数组 168 ms，`VersionedQueue` 1 ms。边界：版本分叉（同一旧版本后接两个不同 push）。
