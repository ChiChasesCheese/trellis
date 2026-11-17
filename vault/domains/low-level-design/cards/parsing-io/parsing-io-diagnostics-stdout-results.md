---
id: parsing-io-diagnostics-stdout-results
node: parsing-io.diagnostics
type: qa
step: 1
---
## Q
命令行工具读一行写一行结果，下游用管道逐行解析。开发时在处理中间 `print("bad row 3")`，为什么会让下游崩掉？诊断信息该写到哪里？

## A
**标准输出只放结果，诊断走标准错误**

- **两条流**：stdout 是程序的产物，会被管道、重定向、别的程序读；stderr 是给人看的，不进管道；
- **混写的后果**：下游把「bad row 3」当成一条结果去解析，报错或者更糟，悄悄解析成一条垃圾记录；
- **`logging` 的默认**：`logging.basicConfig()` 的处理器写到 stderr，所以用 `logging` 不会污染 stdout；`print` 默认写 stdout，要诊断就写 `print(..., file=sys.stderr)`；
- **测试**：捕获 stdout，逐行断言都是合法的结果行；多一行杂音就失败；
- **日志不是错误响应**：坏行的错误结果仍然作为一行写进 stdout（`{"error": ...}`），日志里只放运维要看的细节。

```python
import subprocess, sys

child = "import logging; logging.basicConfig(); print('result'); logging.warning('bad row 3')"
r = subprocess.run([sys.executable, "-c", child], capture_output=True, text=True)
print(repr(r.stdout))     # 'result\n'：管道下游只会看到这一行
print(repr(r.stderr))     # 'WARNING:root:bad row 3\n'：给人看
```

**知识点：**日志与诊断输出（Logging）
