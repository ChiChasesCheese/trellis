---
id: testing-testable-design-none-default
node: testing.testable-design
type: qa
step: 5
---
## Q
函数从环境变量读区域设置，为了便于测试允许传入一个 `environment` 字典。写成 `env = environment or os.environ`，测试传入空字典时为什么读到了真实环境？

## A
**缺省才用默认值：判断 `is None`，不是真假**

- **空字典是假值**：`{} or os.environ` 得到 `os.environ`；调用方明明传了一个「什么都没有」的环境，却被换成了真实环境；
- **后果**：测试在你的机器上通过（环境里恰好没有这个变量），在 CI 上失败；或者反过来，测试结果取决于运行它的人的 shell；
- **正确写法**：`environment if environment is not None else os.environ`；空映射也算调用方给了；
- **同一个原则适用于**：时钟、随机源、存储，凡是「可注入、有默认」的参数；
- **默认值读取要晚**：不要把 `os.environ` 或 `time.time()` 的结果写成函数默认参数，它在定义时只求值一次。

```python
import os

def region(environment=None) -> str:
    env = os.environ if environment is None else environment
    return env.get("REGION", "us")

os.environ["REGION"] = "eu"
print(region({}), region({"REGION": "ap"}), region())     # us ap eu
print(({} or os.environ).get("REGION"))                    # eu：错误写法读到了真实环境
```

**知识点：**可测的设计（Design for Testability）
