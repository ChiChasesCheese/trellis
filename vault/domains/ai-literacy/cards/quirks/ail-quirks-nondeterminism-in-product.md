---
id: ail-quirks-nondeterminism-in-product
node: quirks.nondeterminism
type: qa
step: 3
---
## Q
你的自动化测试把模型的回答当作期望值逐字比较，隔三差五红灯。该怎么改？

## A
**别假设同一输入会得到同一输出；把"必须相同"放在结构和判断上，而不是逐字上。**

- **断言结构：** 让模型输出 JSON，解析后断言字段（分类标签、金额），不比整段文字。
- **多次运行看通过率：** 一个用例跑 N 次，统计通过率；单次通过或失败说明不了什么。
- **要可复现就录像：** 把第一次的请求和响应存下来，测试时回放，不再调用模型。
- **别信温度 0：** 即使自己部署，批大小一变，结果也会变。
- **改输出方式：** 能用工具调用或约束输出的格式，就不要让它自由写。

```python
import hashlib

def cached(prompt, call, store):
    key = hashlib.sha256(prompt.encode()).hexdigest()
    if key not in store:
        store[key] = call(prompt)
    return store[key]
```

测试里用 `cached`：第一次真调模型，之后同一个提示直接取存下的回答，用例才稳定。真正评估模型质量时，则要关掉缓存，多跑几次看比例。
