---
id: ai-risks-new-dependency
node: ai.risks
type: qa
step: 4
---
## Q
智能体改完代码，依赖列表里多了一个你没见过的包。为什么要先停下查，而不是让测试跑过就算？

## A
**每个新增依赖，都要确认是你要的那个**

- **名字不是证据**：公共包索引允许任何人注册没被占用的名字，拼写相近的包可能是另一个东西；
- **有没有必要**：标准库能不能解决，几行代码和一个依赖，后者要永久维护；
- **来源与版本**：包的发布者、版本是否固定，锁文件是不是也更新了；
- **机械做法**：读依赖文件，比较前后，只把新增的名字列出来再逐个查；
- **这是风险管理的做法**，不是对某个具体包的判断。

```python
import tomllib

def deps(text: str) -> set[str]:
    spec = tomllib.loads(text)["project"]["dependencies"]
    return {d.split(">")[0].split("=")[0].split("<")[0].strip() for d in spec}

before = 'project = {name = "x", dependencies = ["requests>=2.31"]}'
after = 'project = {name = "x", dependencies = ["requests>=2.31", "requestz>=1.0"]}'
print(deps(after) - deps(before))          # {'requestz'}：先查它是什么
```

**知识点：**风险与权限（Risks & Guardrails）
