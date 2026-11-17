---
id: errors-narrow-no-swallow
node: errors.narrow-catch
type: qa
step: 5
---
## Q
缓存刷新写成 `try: cache["v"] = load()` 加 `except Exception: pass`，“反正失败了就继续用旧值”。这样写的问题在哪？一个 `except` 块可以合法地做什么？

## A
**捕获以后只有三件合法的事：处理、翻译、重新抛出**

- **`pass` 吞掉了所有东西**：超时我们预料到了，可 `load()` 里的拼写错误（`NameError`）也被一起吞了，缓存永远是旧值，没有任何信号；
- **处理**：有明确的降级办法，如超时就沿用旧值，并留一条日志，让人知道用的是旧数据；
- **翻译**：换成合同里的异常，写 `raise ServiceError(...) from exc`，保留原因；
- **重新抛出**：清理完后 `raise`，让能决定的人决定；
- **只列预期的类型**：吞掉的范围越窄，吞错东西的机会越小。

```python
def load(): return undefined_name             # 缺陷：NameError

def refresh_bad(cache):
    try: cache["v"] = load()
    except Exception: pass                    # 缺陷也被吞：旧值悄悄一直用

def refresh_good(cache):
    try: cache["v"] = load()
    except TimeoutError: print("超时：沿用旧值")   # 预期的失败：降级并留痕

c = {"v": 1}
refresh_bad(c); print("bad 没有任何报错，c =", c)
try: refresh_good(c)
except NameError: print("good：缺陷露出来了")
```

**知识点：**捕获的范围（Narrow Catch）
