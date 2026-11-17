---
id: ai-risks-secrets-in-argv
node: ai.risks
type: qa
step: 3
---
## Q
让智能体运行一个需要 API 密钥的脚本，可以把密钥写在命令行参数里吗？应该怎么传、怎么查看？

## A
**密钥不放参数、不进对话、不进仓库**

- **参数是公开的**：macOS 和默认配置的 Linux 上，同机其他用户能用 `ps` 看到命令行参数（Linux 可用 `hidepid` 挂载选项收紧）；人手敲的命令还会进 shell 历史；
- **输出会进对话**：智能体读到的命令输出会成为它的上下文，打印出的密钥就留在记录里；
- **传法**：用环境变量或权限为 `0600` 的文件，不出现在 `args` 列；同一用户下的进程仍然能读，所以它不是保密措施，只是不泄露到别处；
- **查看时只看键名**：只列出名字，不打印值；
- **仓库**：密钥文件加进忽略列表，提交前检查 diff。

```python
import subprocess, sys

idle = "import time; time.sleep(5)"
p = subprocess.Popen([sys.executable, "-c", idle, "sk-demo-123"])   # 密钥放在参数里
shown = subprocess.run(["ps", "-o", "args=", "-p", str(p.pid)],
                       capture_output=True, text=True).stdout
print(shown.split()[-1])                      # sk-demo-123：ps 能看到参数
p.terminate()

env = {"API_KEY": "sk-demo-123"}
print(sorted(env))                            # ['API_KEY']：查看时只看键名
```

**知识点：**风险与权限（Risks & Guardrails）
