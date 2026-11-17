---
id: errors-narrow-short-try
node: errors.narrow-catch
type: qa
step: 1
---
## Q
校验一个过期时间参数，`try` 应该包住整个函数体，还是只包住 `float(raw)` 那一句？`except` 里该列什么？

## A
**`try` 只包会抛的那一句，`except` 只列预期的类型**

- **`try` 越短，`except` 越可信**：块里只有一句，抓到的异常就一定出自这一句；块里有十行，任何一行的 bug 都会被当成“参数不合法”；
- **后续判断放在 `try` 外面**：范围检查、业务规则不会抛我们预期的那类异常，不需要保护；
- **类型列全**：`float("abc")` 抛 `ValueError`，`float(10**400)` 抛 `OverflowError`（整数太大转不了浮点数），漏掉后者，一个特制请求就能打出 500；
- **用 `except (A, B)` 而不是 `except Exception`**：前者是“我知道会发生什么”，后者是“我不知道，先吞掉”；
- **成功路径放进 `else` 或写在 `try` 后面**，别塞进 `try`。

```python
def ttl_ok(raw) -> bool:
    try:
        ttl = float(raw)                       # 只包住会抛的这一句
    except (ValueError, OverflowError):        # 10**400 抛 OverflowError
        return False
    return 0 < ttl < 86400                     # 判断在 try 外面

print(ttl_ok("60"), ttl_ok("abc"), ttl_ok(10**400), ttl_ok("-1"))   # True False False False
```

**知识点：**捕获的范围（Narrow Catch）
