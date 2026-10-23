---
id: hl-c14-cv-any-stop
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 13
---
## Q
怎样让阻塞在条件变量上的线程也能被 `stop_token` 取消？写出 `waiter`。

## A
用 `std::condition_variable_any` 的 `wait(lock, stop_token, pred)`：被取消时也能从阻塞等待中醒来，**返回 false**。

```cpp
struct Mailbox {
    std::mutex m;
    std::condition_variable_any cv;     // _any：wait 可接收 stop_token
    int pending = 0;
};
void waiter(std::stop_token st, Mailbox& mb, bool& woke_by_stop) {
    std::unique_lock lk(mb.m);
    bool got = mb.cv.wait(lk, st, [&] { return mb.pending > 0; });
    woke_by_stop = !got;                // 返回 false = 先被请求停止
}
```
- 实测：阻塞的 waiter 被 stop 请求唤醒。
