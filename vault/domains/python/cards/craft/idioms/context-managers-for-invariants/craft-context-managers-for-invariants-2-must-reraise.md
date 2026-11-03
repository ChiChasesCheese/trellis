---
id: craft-context-managers-for-invariants-2-must-reraise
node: craft.idioms.context-managers-for-invariants
type: qa
step: 2
---
## Q
**上下文管理器守不变量 · `@contextmanager` 里 `except BaseException` 之后不写 `raise` 会怎样**｜写法

用生成器写的上下文管理器，在 `yield` 外面包一层 `try / except BaseException` 做失败清理，忘了在末尾 `raise`。程序看起来还在正常跑，会出什么问题？有没有更不容易写错的写法？

## A
**要点。** `with` 块里抛出的异常，会被传回管理器生成器里 `yield` 的位置。生成器如果在 `except` 里处理完就正常结束，`contextlib` 会认为「管理器吞掉了这个异常」，`with` 之后的代码照常往下执行，调用方以为成功了。清理完要交还异常就必须 `raise`。

```python
@contextmanager
def swallow():
    try:
        yield
    except BaseException:
        print("  清理一下")               # 忘了 raise：异常被吞掉了

@contextmanager
def reraise():
    try:
        yield
    except BaseException:
        print("  清理一下")
        raise                              # 清理完交还给调用方

@contextmanager
def finally_only():
    try:
        yield
    finally:
        print("  清理一下")               # 只清理不拦截：不写 except 最不容易错

for cm in (swallow, reraise, finally_only):
    print(cm.__name__)
    try:
        with cm():
            raise ValueError("业务失败")
        print("  with 之后继续执行: 调用方以为成功了")
    except ValueError:
        print("  调用方收到 ValueError")
```

实际输出：

```
swallow
  清理一下
  with 之后继续执行: 调用方以为成功了
reraise
  清理一下
  调用方收到 ValueError
finally_only
  清理一下
  调用方收到 ValueError
```

**为什么。** 最不容易写错的是只写 `finally`：它只清理，不拦截，异常自然继续传播。只有「失败」和「成功」的收尾不同（失败释放键，成功保留结果）时才需要 `except`，而那时的规则就是：清理之后 `raise`。

**易错。** 捕获 `BaseException` 而不是 `Exception`：这里管理器守的是资源，`KeyboardInterrupt` 之类也应该触发释放；但前提是处理完之后仍然重新抛出，否则 Ctrl-C 也被吞了。
