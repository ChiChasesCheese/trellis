---
id: errors-narrow-exception-not-base
node: errors.narrow-catch
type: qa
step: 2
---
## Q
想“兜底”时，裸 `except:`、`except BaseException`、`except Exception` 有什么区别？为什么服务代码里最多只写到 `except Exception`？

## A
**兜底最宽到 `Exception`，不碰 `BaseException`**

- **`BaseException` 比 `Exception` 多出几个“不是失败”的成员**：用户按下 Ctrl-C 的 `KeyboardInterrupt`、程序主动退出的 `SystemExit`、生成器关闭时的 `GeneratorExit`，异步任务被取消的 `asyncio.CancelledError` 也在其中；
- **裸 `except:` 等于 `except BaseException`**：用户按了 Ctrl-C，进程却把它当成普通错误处理掉，程序停不下来；
- **`except Exception` 不拦它们**：中断和退出照常穿过，只翻译业务上的失败；
- **线程池要小心**：工作线程里的 `BaseException` 会被 `Future` 存起来，需要在取结果的地方让它重新冒出来，别吞；
- **真要捕获 `BaseException`**：只为清理，处理完必须 `raise`。

```python
print(issubclass(ValueError, Exception), issubclass(KeyboardInterrupt, Exception))   # True False

def bare():
    try: raise KeyboardInterrupt
    except: return "吞掉了 Ctrl-C"             # 裸 except 一并接住

def translate():
    try: raise KeyboardInterrupt
    except Exception: return "翻译成错误"

print(bare())
try: translate()
except KeyboardInterrupt: print("Ctrl-C 照常穿过")
```

**知识点：**捕获的范围（Narrow Catch）
