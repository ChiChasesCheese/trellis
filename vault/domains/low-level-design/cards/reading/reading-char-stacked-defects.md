---
id: reading-char-stacked-defects
node: reading.characterization
type: qa
step: 4
---
## Q
一个函数里叠着两个缺陷：违规计数从 0 开始漏掉了第一条，另一个把阈值比较写成了 `>`。同时修完再看测试，哪里不对劲你也说不清。该怎么修？

## A
**一次只修一个缺陷：每修一个，只允许对应的那几个钉住的值变化**

- **先钉住现状，包括两个缺陷造成的错值**；
- **修第一个缺陷**：重新跑，只有和它有关的输入的输出变了，其余必须不变；这几个变化就是你的修改清单，有意地更新对应的期望；
- **再修第二个**：同样的做法，对照第二批变化；
- **同时修两个的后果**：变化混在一起，一个输入变了，说不清是谁的功劳，更看不出是不是第三个问题；
- **每个缺陷一次提交**：出问题时可以精确回退，评审的人也看得懂。

```python
def violations(events):
    n = 0
    for e in events[1:]:                 # 缺陷 A：漏掉第一条
        n += e == "bad"
    return n

def blocked(events, limit=3):
    return violations(events) > limit    # 缺陷 B：阈值边界，应是 >=

cases = [["bad"] * k for k in (0, 1, 3, 4)]
print([(len(c), violations(c), blocked(c)) for c in cases])
# [(0, 0, False), (1, 0, False), (3, 2, False), (4, 3, False)]
# 先修 A：计数变成 0、1、3、4，4 件的那一项变成 blocked
# 再修 B：3 件的那一项也变成 blocked；每一步的变化都能逐项解释
```

**知识点：**特征测试（Characterization Tests）
