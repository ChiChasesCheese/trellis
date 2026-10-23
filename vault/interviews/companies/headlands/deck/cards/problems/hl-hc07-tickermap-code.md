---
id: hl-hc07-tickermap-code
node: problems.hc07-ticker-hash-map
type: qa
step: 7
---
## Q
手写 `TickerMap` 的 `find` 和 `upsert` 核心代码怎么写？`rehash` 和 `remove` 呢？

## A
数据：`String[] keys; long[] vals;`，`null` = 空格，`TOMB` = 墓碑，容量 2 的幂，`home(key) = (hashCode * 0x9E3779B9) >>> shift`。

```java
private int find(String key) {
    int i = home(key);
    while (true) {
        String k = keys[i];
        if (k == null) return -1;
        if (k != TOMB && k.equals(key)) return i;
        i = (i + 1) & mask;
    }
}
private OptionalLong upsert(String key, long value, boolean accumulate) {
    int i = home(key), firstTomb = -1;
    while (true) {
        String k = keys[i];
        if (k == null) break;
        if (k == TOMB) { if (firstTomb < 0) firstTomb = i; }
        else if (k.equals(key)) {
            long old = vals[i];
            vals[i] = accumulate ? Math.addExact(old, value) : value;
            return OptionalLong.of(old);
        }
        i = (i + 1) & mask;
    }
    if (firstTomb >= 0) { /* 复用墓碑：写入，size++，tombs-- */ return OptionalLong.empty(); }
    if ((size + tombs + 1) * 2 > keys.length) { rehash(); i = home(key); while (keys[i] != null) i = (i + 1) & mask; }
    keys[i] = key; vals[i] = value; size++;
    return OptionalLong.empty();
}
```
`remove`：`find` 后 `keys[i] = TOMB; vals[i] = 0; size--; tombs++`。`rehash`：`allocate(capacityFor(size, 4))`，只搬活条目（跳过 `null` 和 `TOMB`），重新算 `home`，搬时不需比较。

要点：复用墓碑不改变 size+tombs，不需检查 resize；占用空格使已用 +1，先检查；`Math.addExact` 先算后写，溢出时表未被改动；`while (true)` 不会死循环因为保证 `(size + tombs) × 2 ≤ capacity`。`TickerMap.add` 先 upsert 再 find 多一次探测，热路径应只探测一次。20 万代码 100 万次 `add` 约 42–48 ms。
