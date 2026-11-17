---
id: ai-specs-state-your-decisions
node: ai.specs
type: qa
step: 4
---
## Q
合同没规定“请求里用户不存在、数量也非法”时先报哪个错。让智能体实现时，这件事该怎么处理？

## A
**合同没写的决定，自己定，写进指令**

- **没写的决定总会被实现选掉**：检查顺序、边界归属（含不含两端）、取整规则、失败时是否留下痕迹、空输入怎么算；
- **选哪边是碰运气**：同一个输入，两种实现返回不同的错误码，测试和调用方都会因此变红；
- **做法**：开工前把这几项各定一个答案，写进第一条指令，并配一个同时违反两条规则的例子；
- **定不下来**：向出题人（或产品方）问，问不到就自己定，并把假设写在代码注释和回答里。

```python
USERS = {"bob"}

def create_a(user, qty):                  # 先查用户
    if user not in USERS: return 404
    if qty <= 0: return 400
    return 201

def create_b(user, qty):                  # 先校验输入
    if qty <= 0: return 400
    if user not in USERS: return 404
    return 201

print(create_a("eve", 0), create_b("eve", 0))     # 404 400
```

<details class="pt"><summary>延伸</summary>

常见的约定是格式错误先于“资源不存在”，因为前者不用读存储；但它是约定，不是定律。合同写了别的顺序就听合同的，关键是指令里要有一个“两个都违反”的例子来钉住它。

</details>

**知识点：**写清任务（Specifying the Task）
