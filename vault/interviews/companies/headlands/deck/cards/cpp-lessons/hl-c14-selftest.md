---
id: hl-c14-selftest
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 18
---
## Q
自测：`std::thread t(f);` 之后函数直接返回会怎样？`cv.wait(lk)` 不带谓词有哪两个风险？

## A
- 析构时线程仍 joinable，调用 `std::terminate`。
- 不带谓词的风险：①**虚假唤醒**；②通知先于等待时（通知丢失）永远睡眠。应在锁内检查谓词。
