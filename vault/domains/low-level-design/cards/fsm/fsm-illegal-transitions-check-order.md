---
id: fsm-illegal-transitions-check-order
node: fsm.illegal-transitions
type: qa
step: 2
---
## Q
别人对一笔待放款的贷款发起还款，应当报“无权限”还是“状态不对”？多个检查都不通过时，顺序按什么定？

## A
**归属先于状态，状态先于余额**

- **归属在前**：先问“你有没有权限碰这笔贷款”，没有就是 403；若先报状态错误，等于告诉陌生人这笔贷款存在、是什么状态；
- **状态与超额在中**：贷款不是 `active`，或还款超过未还金额，都是 409 invalid_state；
- **余额在后**：它读的是另一个对象，条件满足了才有必要读；
- **顺序要固定，写进测试**：测试用“同时违反两条规则”的输入，调换两行代码，测试必须变红。

```python
LOAN = {"borrower": "mia", "state": "pending", "remaining": 100}

def repay(caller, amount, balance):
    if type(amount) is not int or amount <= 0: return 400
    if caller != LOAN["borrower"]: return 403                   # 归属
    if LOAN["state"] != "active" or amount > LOAN["remaining"]: return 409
    if balance < amount: return 409                             # 余额不足（另一个错误码）
    return 200

print(repay("eve", 10, 0), repay("mia", 10, 500))               # 403 409
```

<details class="pt"><summary>延伸</summary>

上面最后一个 409 与状态错误的 409 码相同、原因不同，真实合同里它们是两个不同的错误名（`invalid_state` 与 `insufficient_balance`），调用方才能区分。

</details>

**知识点：**非法转移与幂等（Illegal Transitions）
