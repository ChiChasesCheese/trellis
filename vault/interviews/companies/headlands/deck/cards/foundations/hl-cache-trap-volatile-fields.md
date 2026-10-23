---
id: hl-cache-trap-volatile-fields
node: foundations.cpu-cache-locality
type: qa
step: 42
---
## Q
判断：两个线程分别对同一对象里两个**不同**的 `volatile long` 字段高频自增，所以不存在共享问题。对吗？

## A
错。两个字段在对象不大时很可能落在同一个缓存行，产生伪共享：「不同变量」不等于「不同缓存行」。

解决：拆到不同缓存行（`@Contended` 或填充），或每个线程用独立并填充的对象，或改用 `LongAdder`。
