---
id: concurrency-check-then-act
node: concurrency.model
type: qa
step: 3
---
## Q
```python
if key not in cache:
    cache[key] = expensive_build(key)
```
`dict` 的单次读写在 CPython 里都是原子的，那这段代码在多线程下还有 bug 吗？

## A
有。`in` 检查和 `[key] =` 赋值是**两条**独立的字节码级操作，中间可以被切换到另一个线程；两个线程都可能在对方写入之前通过了 `not in` 检查，于是都调用了一次 `expensive_build(key)`，后写入的那次覆盖掉先写入的——这是一次典型的 check-then-act 竞态（race），不是字典本身不安全,是"先查后做"这个复合动作不安全。

修法：用一把 `threading.Lock` 把检查和写入一起罩住，或者干脆用 `cache.setdefault(key, expensive_build(key))`（注意它仍会无条件先算出 `expensive_build(key)`，真正省重复计算要靠锁或 `functools.cache`）。
