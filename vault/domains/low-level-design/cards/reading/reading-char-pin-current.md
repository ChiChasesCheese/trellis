---
id: reading-char-pin-current
node: reading.characterization
type: qa
step: 1
---
## Q
接手一段没有测试的运费计算代码，要给它加功能。你不确定某些输入下它“应该”返回什么。动手改之前应该先写什么测试？期望值怎么定，哪怕现在的行为看起来不对？

## A
**特征测试（characterization test）：把现在的行为原样钉住，再改**

- **目的不是证明代码对，而是知道你改了什么**：改完以后，任何一个钉住的值变了，都是你有意或无意改变了行为；
- **期望值来自运行结果**：用一批输入跑一遍现有代码，把输出写进断言；这与“按规格手写期望”的新功能测试是两回事；
- **每个值逐个过目**：觉得对的当作规格，觉得可疑的照样钉住，但在注释里标成“可疑”；
- **不要顺手修**：重构时发现的 bug 另开一次修改；同一次改动里既重构又修缺陷，测试变红时分不清是谁；
- **先覆盖边界**：每一档的上沿下沿、零、负数、空输入；缺陷最爱住在边界。

```python
def shipping(kg):                      # 遗留代码
    if kg < 1: return 5
    if kg < 5: return 9
    return 9 + (kg - 5) * 2

def test_pins_current_behaviour():
    assert shipping(0.5) == 5
    assert shipping(1) == 9            # 边界：1 公斤属于第二档
    assert shipping(5) == 9
    assert shipping(7) == 13
    assert shipping(-3) == 5           # 可疑：负重量不报错；先钉住，另行处理

test_pins_current_behaviour(); print("现状已钉住")
```

**知识点：**特征测试（Characterization Tests）
