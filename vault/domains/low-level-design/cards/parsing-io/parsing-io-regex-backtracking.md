---
id: parsing-io-regex-backtracking
node: parsing-io.regex
type: qa
step: 4
---
## Q
一个校验正则 `(a+)+$` 在输入 `"aaaa…ab"` 上，每多一个 `a` 耗时翻一倍，几十个字符就把服务卡死。为什么？怎么改？

## A
**嵌套量词会指数回溯，改成没有歧义的写法**

- **贪婪（greedy）**：`+` 先尽量多吃，后面失败再一个一个吐出来重试；
- **回溯（backtracking）**：`(a+)+` 把 n 个 `a` 切成若干段的方式有 2^(n-1) 种；末尾的 `b` 让每一种都失败，引擎把它们全试一遍；
- **ReDoS**：用户可控的输入遇上这样的模式，几十个字符就能让一个线程卡住很久，是一种拒绝服务攻击；
- **改法**：去掉嵌套（`a+$`），或者让相邻的部分不能匹配同一批字符；
- **3.11 的工具**：原子组 `(?>...)` 和占有量词 `a++`，匹配成功后不再吐回去，失败得快；
- **更根本的**：限制输入长度，先检查长度再跑正则。

```python
import re, time

def cost(pattern: str, n: int) -> float:
    start = time.perf_counter()
    re.match(pattern, "a" * n + "b")
    return time.perf_counter() - start

print(cost(r"(a+)+$", 22) / cost(r"(a+)+$", 20))   # 约 4：每多一个 a 翻倍
print(cost(r"a+$", 5000) < 0.01)                    # True：线性
```

**知识点：**正则表达式（Regular Expressions）
