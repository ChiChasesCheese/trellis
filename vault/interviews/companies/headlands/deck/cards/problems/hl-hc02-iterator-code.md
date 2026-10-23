---
id: hl-hc02-iterator-code
node: problems.hc02-merge-k-streams
type: qa
step: 8
---
## Q
写出惰性合并迭代器的核心代码：堆的比较器、`prime()`、`advance()`、`next()`。

## A
```java
heap = new PriorityQueue<>(Math.max(1, snapshot.size()),
    Comparator.<Head<T>, T>comparing(h -> h.value).thenComparingInt(h -> h.stream));

void prime() {
    if (!started) { started = true;
        for (int i = 0; i < snapshot.size(); i++) {
            var h = new Head<T>(i, snapshot.get(i));
            if (advance(h, null)) heap.add(h); } }
    if (lastEmitted != null) {
        var h = lastEmitted; lastEmitted = null;
        if (advance(h, h.value)) heap.add(h); }
}
boolean advance(Head<T> h, T prev) {
    if (!h.source.hasNext()) return false;
    T next = Objects.requireNonNull(h.source.next());
    if (prev != null && next.compareTo(prev) < 0)
        throw new UnsortedInputException(h.stream, h.position + 1);
    h.value = next; return true;
}
public T next() {
    prime(); Head<T> h = heap.poll();
    if (h == null) throw new NoSuchElementException();
    lastEmitted = h; return h.value;
}
```
要点：比较器先值后编号就是「稳定」；`PriorityQueue` 初始容量不能为 0，故 `Math.max(1, …)`；`snapshot = List.copyOf(sources)` 防调用者之后修改；`Iterator` 协议要求耗尽后 `next()` 抛 `NoSuchElementException`；显式 `<Head<T>, T>` 因 lambda 参数类型推不出。
