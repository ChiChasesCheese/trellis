---
id: ai-delegation-trust-the-exit-code
node: ai.delegation
type: qa
step: 6
---
## Q
智能体回复“所有问题都修好了，测试通过”。交出去之后，收口时你该看什么？

## A
**以命令的退出码和输出为准，不以它的自述为准**

- **指令里的三句**：只改这个函数、不动测试、不动公开签名；改完立刻运行测试；
- **收口**：自己跑一遍全量测试，看退出码和失败数；`0` 才是通过；
- **再读 diff**：范围外有没有文件被改，测试文件有没有被动；
- **它没有跑的东西**：并发、边界、你自己补的用例，都要自己再跑；
- **原因**：自述是一段文字，退出码是程序给出的结果。

```python
import subprocess, sys

claim = "全部修好，测试通过"
r = subprocess.run([sys.executable, "-c", "assert 1 + 1 == 3"],
                   capture_output=True, text=True)
print(claim, "| exit code:", r.returncode)               # 1
print(r.stderr.strip().splitlines()[-1])                 # AssertionError
```

**知识点：**该交给 AI 还是自己写（When to Delegate）
