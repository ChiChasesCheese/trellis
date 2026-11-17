---
id: refactoring-abs-straight-line
node: refactoring.over-abstraction
type: qa
step: 3
---
## Q
对账要分三级匹配一笔付款：先按引用号，再按金额加日期，最后按付款人名。有人想用“策略模式加责任链”来写，每级一个类。这个固定的三步为什么写成直线代码更好？

## A
**步骤固定且只有一处使用，顺序写下来就是最清楚的文档**

- **三级、固定顺序、不会被配置**：不存在“运行时换策略”的需求，模式的灵活性用不上；
- **直线代码从上到下读完就懂**：优先级、先后、回退都在眼前；类加链要在三个文件之间跳；
- **模式的成本是实打实的**：基类、三个子类、组装链的代码；少一个环节时还要想“这条链是怎么拼起来的”；
- **什么时候该用**：规则会由配置或插件增删、会有十几种、要在不同流程里复用同一组策略；
- **每一级仍可以是一个小函数**：直线代码也能拆函数，这是普通的函数拆分，不需要类层次。

```python
def match(pay, ledger):
    for e in ledger:                                   # 第一级：引用号
        if e["ref"] == pay["ref"]: return e, "ref"
    for e in ledger:                                   # 第二级：金额 + 日期
        if (e["amount"], e["day"]) == (pay["amount"], pay["day"]): return e, "amount_day"
    for e in ledger:                                   # 第三级：付款人
        if e["payer"].lower() == pay["payer"].lower(): return e, "payer"
    return None, "none"

ledger = [{"ref": "r1", "amount": 5, "day": 1, "payer": "Ann"}]
print(match({"ref": "x", "amount": 9, "day": 3, "payer": "ANN"}, ledger)[1])   # payer
```

**知识点：**过度抽象（Over-Abstraction）
