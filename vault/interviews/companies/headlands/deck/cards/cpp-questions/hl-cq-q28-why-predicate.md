---
id: hl-cq-q28-why-predicate
node: cpp-questions.g-concurrency
type: qa
step: 3
---
## Q
`condition_variable::wait` 为什么必须带谓词？`wait(lk, pred)` 等价于什么写法？

## A
- `wait` 可能**虚假唤醒**（没人 notify 也醒来）；也可能在你重新拿到锁之前，条件又被别的线程改掉。
- 所以醒来后必须重新检查条件。
- `wait(lk, pred)` 等价于 `while (!pred()) wait(lk);`。
