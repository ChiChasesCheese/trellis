---
id: testing-partitioning-one-invalid-at-a-time
node: testing.partitioning
type: qa
step: 4
---
## Q
订单校验函数先查数量、再查单价，两个都不合法就抛第一个错。测试写成 `validate(0, -5)`，期望抛“qty”错误，通过了。这个测试为什么挡不住“单价检查被误删”？无效输入的用例应该怎么挑？

## A
**一个用例只放一个无效值，其余都合法**

- **错误屏蔽（error masking）**：先触发的检查会遮住后面的检查；`(0, -5)` 里单价检查从未执行，删掉它测试照样绿；
- **每个无效类各一个用例**：数量无效配合合法单价，单价无效配合合法数量，每个检查单独被证明有效；
- **合法的基准值要固定**：先选一组全部合法的值（数量 1、单价 100），每次只把其中一个换成无效类的代表，失败时一眼看出是谁；
- **组合无效是另一类问题**：同时多个字段无效时要不要一次返回全部错误，是规格里的行为，有就单独写一个用例；
- **等价类的清单随之变多**：每个参数的无效类相加，不是相乘，用例数仍然可控。

```python
def validate(qty, price):
    if qty < 1: raise ValueError("qty")
    if price <= 0: raise ValueError("price")   # 假设这一行被误删
    return qty * price

def err(*args):
    try: validate(*args)
    except ValueError as e: return str(e)

print(err(0, -5))     # qty：删掉价格检查，这条照样通过
print(err(1, -5))     # price：删掉价格检查就会变成 None，测试红
```

<details class="pt"><summary>延伸</summary>

反过来，对“全部错误一起返回”的校验器（表单、批量导入），多个无效字段同时出现正是要测的行为：断言返回的错误集合包含每个字段，而不是只看第一个。

</details>

**知识点：**用例选择（Partitioning & Boundaries）
