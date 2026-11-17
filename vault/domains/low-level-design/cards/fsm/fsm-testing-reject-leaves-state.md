---
id: fsm-testing-reject-leaves-state
node: fsm.testing
type: qa
step: 2
---
## Q
测非法转移时，只断言“抛了异常”够吗？还要断言什么？

## A
**拒绝之后，状态与数据都和之前一模一样**

- **先改后查的缺陷**：函数先改了数据，再发现状态不对才抛错；调用方看到异常，库里已经有半个改动；
- **断言**：拒绝之前对整个对象做一份深拷贝，拒绝之后比较，必须相等；
- **覆盖所有非法格**：对穷举表里每个拒绝的格子都跑一遍；
- **同理适用于多步操作**：批次里有一步失败，整批的状态不变。

```python
import copy

def repay(loan, amt):
    loan["remaining"] -= amt                            # 缺陷：先改数据
    if loan["state"] != "active": raise ValueError("illegal")

loan = {"state": "pending", "remaining": 100}
before = copy.deepcopy(loan)
try: repay(loan, 30)
except ValueError: pass
print(loan == before, loan)           # False {'state': 'pending', 'remaining': 70}
```

<details class="pt"><summary>延伸</summary>

修法是“先检查，再写”：所有可能失败的检查放在第一次写入之前；做不到时，写入放进事务，失败就回滚。

</details>

**知识点：**状态机的穷尽测试（Exhaustive Testing）
