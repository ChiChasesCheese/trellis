---
id: condition-while-not-if
node: concurrency.locks-races
type: qa
source: python-docs
---
## Q
用 `Condition`（条件变量）实现生产者-消费者时，等待方为什么要写成 `while not 条件: cv.wait()`，而不是 `if not 条件: cv.wait()`？

## A
`wait()` 被 `notify()` 唤醒后只是重新获得锁并返回，并不保证此时条件仍然成立：`notify()` 可能唤醒了多个等待者中的一个，其它线程可能先一步把资源又消费掉，或者条件本来就是被间接触发的宽泛信号。用 `while` 循环在被唤醒后重新检查条件，条件不满足就继续 `wait()`，才能避免“被虚假唤醒后仍按不满足的条件继续执行”的 bug；`wait_for(predicate)` 就是对这个循环的封装。
