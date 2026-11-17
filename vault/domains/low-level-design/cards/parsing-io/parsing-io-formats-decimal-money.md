---
id: parsing-io-formats-decimal-money
node: parsing-io.formats
type: qa
step: 4
---
## Q
接口返回 `{"amount": 0.10}` 和 `{"tip": 0.20}`，累加金额得到 0.30000000000000004。JSON 里的金额和很大的整数怎么读才不丢精度？

## A
**金额读成 Decimal，大整数 Python 本来就精确**

- **`float` 是二进制近似**：0.1 与 0.2 都没有精确表示，相加有误差；金额不能用它；
- **`parse_float=Decimal`**：`json.loads` 遇到小数写法的数字时，用 `Decimal(原文)` 构造，保留原来的十进制位数；
- **整数**：Python 的 `int` 任意精度，`9007199254740993`（2^53 + 1）读出来原样不变；JavaScript 一端会变成 `...992`，所以跨语言接口里把大 ID 写成字符串；
- **更常见的做法**：金额存成「分」的整数，根本不出现小数；
- **CSV 里的值全是字符串**：日期、数字都要自己转换，转换错误和格式错误一样处理。

```python
import json
from decimal import Decimal

raw = '{"amount": 0.10, "tip": 0.20, "id": 9007199254740993}'
f = json.loads(raw)
d = json.loads(raw, parse_float=Decimal)
print(f["amount"] + f["tip"])           # 0.30000000000000004
print(d["amount"] + d["tip"], d["id"])  # 0.30 9007199254740993
```

<details class="pt"><summary>延伸</summary>

输出时用 `json.dumps(obj, default=str)` 才能序列化 `Decimal`；`str(Decimal("0.30"))` 保留末尾的 0，对账时位数一致。

</details>

**知识点：**CSV 与 JSON 的稳健读写（CSV & JSON）
