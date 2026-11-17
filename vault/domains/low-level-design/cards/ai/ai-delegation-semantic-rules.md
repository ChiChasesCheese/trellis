---
id: ai-delegation-semantic-rules
node: ai.delegation
type: qa
step: 4
---
## Q
应收款分摊时，每家商户分到的钱要取整到分。为什么“怎么取整”这类语义决定要自己做，而不是让智能体选？

## A
**取整、平局、容差，是合同的一部分**

- **没有对错，只有约定**：半入偶、半进位、向下取整的结果各不相同；总额对不上差的就是一分钱；
- **公开示例常常凑巧一致**：数字没落在 .5 上，三种规则的输出一样；
- **`round` 的默认**：Python 的 `round` 是半入偶，合同要求半进位时，错只出现在恰好 .5 的行；
- **做法**：自己选定规则，写进指令，配一个落在 .5 上的数字例子。

```python
from decimal import Decimal, ROUND_HALF_UP

cents = [Decimal("12.5"), Decimal("13.5"), Decimal("14.5")]
print([round(c) for c in cents])                                   # [12, 14, 14]
print([int(c.quantize(Decimal("1"), ROUND_HALF_UP)) for c in cents])   # [13, 14, 15]
```

<details class="pt"><summary>延伸</summary>

“分摊”还要决定余数给谁：最后一行吃余数、按小数部分从大到小补一分、平局按编号。这三种每一种都守恒，但分到每家的钱不同，所以也要写进例子。

</details>

**知识点：**该交给 AI 还是自己写（When to Delegate）
