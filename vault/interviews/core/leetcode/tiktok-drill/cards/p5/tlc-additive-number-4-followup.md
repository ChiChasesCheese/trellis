---
id: tlc-additive-number-4-followup
node: p5.additive-number
type: qa
step: 4
---
## Q
**LC 306 累加数**｜追问

面试官接着问：（1）要返回具体的累加序列？（2）数字有几百位、语言没有大整数怎么办？（3）把题改成 LC 842：切成斐波那契序列并要求每个数不超过 `2^31 - 1`？

## A
1. **返回序列**：校验时把数收集到列表，成功就返回，失败就丢弃：

```python
def additive_sequence(num: str) -> list[int]:
    n = len(num)
    for i in range(1, n):
        for j in range(i + 1, n):
            if (i > 1 and num[0] == "0") or (j - i > 1 and num[i] == "0"):
                continue
            a, b = int(num[:i]), int(num[i:j])
            seq, k = [a, b], j
            while k < n:
                a, b = b, a + b
                s = str(b)
                if not num.startswith(s, k):
                    break
                seq.append(b)
                k += len(s)
            else:                          # while 正常结束（没有 break）：恰好用完
                return seq
    return []
```
   运行：`"112358"` → `[1, 1, 2, 3, 5, 8]`，`"199100199"` → `[1, 99, 100, 199]`，`"1023"` → `[]`。
2. **没有大整数**：用字符串竖式加法：两个数字字符串从末位对齐，逐位相加带进位，得到和的字符串，再与 `num` 当前位置比较。每次 `O(位数)`，总复杂度同样 `O(n^3)`。Java 里可以直接用 `BigInteger`。
3. **LC 842**：同样枚举前两个数，但每个数必须 `<= 2^31 - 1`，一旦超出就停止；返回的是整个序列，且序列可以是任意长度的斐波那契式（至少三个数）。核心框架和累加数相同。

**Python 提醒**：`for ... else` 的 `else` 在循环**没有被 `break`** 时执行，适合「所有校验通过才算成功」的场景，省掉一个标志变量；但读起来容易误解，面试里写完最好加一行注释。
