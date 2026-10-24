---
id: pl-conc-datarace-unique-gil-illusion
node: concurrency.data-race-freedom
type: qa
step: 6
---
## Q
Python 有 GIL，是不是多线程代码就不需要加锁了？为什么说 GIL 带来的是一种「安全错觉」？

## A
GIL 保护的是**解释器内部**的数据结构：同一时刻只有一个线程执行字节码，所以多个线程一起 `list.append` 不会弄坏列表：
```python
def add():
    for i in range(100_000): lst.append(i)
# 4 threads run add()
print(len(lst))
```
输出：`400000`。每一次 `append` 是单条 C 函数调用，在 GIL 下天然原子。

但 GIL **不保护你的程序逻辑**。线程可以在两条字节码之间、尤其是在任何阻塞调用（I/O、`sleep`、等锁）时被切换，「先检查后操作」的两步之间别的线程就能进来：
```python
balance = 100
def withdraw(amount):
    global balance
    if balance >= amount:          # check
        time.sleep(0.01)            # a blocking call releases the GIL
        balance -= amount           # act
# 8 threads each withdraw(100)
```
输出：`balance = -700`，8 个线程都通过了检查，余额变成 -700。用 `threading.Lock` 把 check 和 act 包在同一个 `with lock:` 里才正确。

为什么是错觉：
1. 很多单步操作碰巧原子（`list.append`、`dict[k] = v`），测试时不出错，让人以为线程安全。
2. 但「读、改、写」组合、先检查后操作、遍历时修改，都不是原子的。切换只发生在特定检查点和默认约 5 毫秒的时间片边界，所以 bug 稀少、难复现。
3. 在 3.13 起的自由线程构建里没有 GIL，这些「碰巧」连单步操作也不能再依赖，容器内部改用细粒度锁，但业务不变量依旧要自己加锁。

结论：GIL 防止的是解释器崩溃，不防止你的 bug。
