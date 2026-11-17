---
id: fluency-idiomatic-rewrite-behaviour-change
node: fluency.idiomatic-rewrite
type: qa
step: 4
---
## Q
评审里有人把 `if delay is None: delay = 30` 改成 `delay = delay or 30`，说更简洁。重试服务里 `delay=0` 表示“立刻重试”，改完之后线上变慢了。哪些“地道”改写会悄悄改变行为，怎么在改之前拦住？

## A
**改写前先用测试钉住行为，真值判断最容易出事**

- **`or` 当默认值**：`0`、`""`、`[]`、`False` 都是假值，被当成“没传”换成默认值；只想处理 `None` 就写 `is None`；
- **`if items:` 代替 `if items is not None:`**：空列表和 `None` 是两种状态，调用方传 `[]` 的意思是“确实没有”；
- **推导式代替循环**：循环里有 `break`、异常处理、副作用，改成推导式后顺序和次数可能变；`dict(pairs)` 合并重复键时，后面的覆盖前面的，和手写的“已有就跳过”不同；
- **生成器代替列表**：只能遍历一次，也不能 `len()`、下标访问；
- **拦住的办法**：改之前先补一个特征测试（characterization test），把 `0`、`""`、`[]`、`None` 各喂一遍，改完仍然绿才算等价。

```python
def delay_old(delay):
    if delay is None:
        delay = 30
    return delay

def delay_new(delay):
    return delay or 30                       # 看起来更地道

for v in (None, 0, 5):
    print(v, delay_old(v), delay_new(v))     # 输入 0：旧版 0，新版 30，行为变了
```

<details class="pt"><summary>延伸</summary>

大范围改写（整个仓库换写法）交给带测试的小步提交，每步只做一类改动，评审才看得出行为没变。

</details>

**知识点：**改写成地道代码（Idiomatic Rewrite）
