---
slug: exclusive-time-of-functions
---
## Q
**LC 636 函数的独占时间**｜Medium

单线程 CPU 的函数日志 `"id:start|end:时间戳"`，`start` 在该时刻起始，`end` 在该时刻末尾，可递归。求每个函数的独占时间（不含调用其他函数的时间）。

## A
**一句话。** 用栈存正在执行的函数，每个事件结算栈顶从 `prev` 到现在的时间。

```python
def exclusive_time(n, logs):
    res = [0] * n
    st = []                        # 栈顶是正在运行的函数
    prev = 0
    for log in logs:
        f, kind, t = log.split(":")
        f, t = int(f), int(t)
        if kind == "start":
            if st:
                res[st[-1]] += t - prev   # 结算被打断的函数
            st.append(f)
            prev = t
        else:
            res[st.pop()] += t - prev + 1 # end 在时刻末尾
            prev = t + 1
    return res
```

**复杂度。** 时间 `O(L)`，空间 `O(n + L)`。

**易错点。**
- `end` 时少加 `1`：`"0:start:0"`、`"0:end:0"` 占 `1` 个单位，示例一会得 `[3,3]`，应为 `[3,4]`。
- `end` 后忘了 `prev = t + 1`：恢复运行的函数被多算，示例二得 `[10]`，应为 `[8]`。

**追问。**
- 为什么不能用「id → 开始时间」字典？：递归时同一函数的多层调用会互相覆盖，必须按栈层存。
- 日志时间戳改成 `start` 也是末尾呢？：则 `end` 时不用加 `1`，`prev = t`。

**同模式。** LC 20 有效的括号、LC 71 简化路径、LC 394 字符串解码、LC 150 逆波兰表达式求值
