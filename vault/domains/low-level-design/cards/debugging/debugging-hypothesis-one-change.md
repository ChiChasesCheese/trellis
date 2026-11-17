---
id: debugging-hypothesis-one-change
node: debugging.hypothesis
type: qa
step: 3
---
## Q
接口在测试环境偶尔失败。你同时升级了依赖、打开了调试日志、加了重试，然后失败不见了。这说明了什么？为什么实验一次只能改一处？

## A
**一次只改一个变量，否则结果无法归因**

- **同时改三处**：失败消失了，你不知道是哪一处起作用，也不知道另外两处有没有副作用；
- **一次改一处，其余不动**：结果变化才能算在这一处头上；
- **反过来做更有力**：把可疑的因素逐个单独打开或关闭，看缺陷跟着谁走；
- **把每次实验记下来**：改了什么、预期、实际；否则两小时后你会重复做已经做过的实验，或者记错了哪次是哪次；
- **“修好了”要能重现“坏的”**：改回去之后缺陷又出现，才算证实了那一处。

```python
import itertools

def fails(retries, verbose):                 # 假设缺陷只由 retries 决定
    return retries == 0

for retries, verbose in itertools.product((0, 3), (False, True)):
    print(f"retries={retries} verbose={verbose} 失败={fails(retries, verbose)}")
# 四种组合里，失败只跟 retries 一起变；只改 verbose 时结果不变：
# retries=0 verbose=False 失败=True / retries=0 verbose=True 失败=True
# retries=3 verbose=False 失败=False / retries=3 verbose=True 失败=False
```

<details class="pt"><summary>延伸</summary>

有些因素会互相作用（只有同时有 A 和 B 才出错），这时一次改一处会看不到。先单独试每个因素，再试组合，别一上来就改一堆。

</details>

**知识点：**假设驱动（Hypothesis-Driven）
