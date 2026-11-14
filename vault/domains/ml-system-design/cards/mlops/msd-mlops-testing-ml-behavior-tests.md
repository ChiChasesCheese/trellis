---
id: msd-mlops-testing-ml-behavior-tests
node: mlops.testing-ml
type: qa
step: 3
---
## Q
模型行为测试（behavioral testing）的三种类型是什么：最低能力测试、不变性测试、方向性测试？用 pytest 给一个客服意图分类模型或大语言模型各写一个例子。

## A
**思路：** 评测集给出一个平均分，但不告诉你模型**哪种能力**缺了。行为测试像软件的单元测试：针对一种具体能力写一组用例，每组单独通过或失败。这个分类来自 NLP 领域的 CheckList 方法。

- **最低能力测试（MFT，minimum functionality test）：** 一组简单、答案明确的用例，模型必须几乎全对。
- **不变性测试（INV，invariance）：** 对输入做一个**不该影响结果**的改动（换人名、换城市、加个错别字、换个说法），输出应保持不变。
- **方向性测试（DIR，directional）：** 对输入做一个**应该朝某个方向影响结果**的改动，输出应朝那个方向变。

```python
import pytest

def test_mft_refund_intent(clf):
    cases = ["我要退款", "怎么申请退钱", "这单能退吗"]
    assert all(clf(t) == "refund" for t in cases)

@pytest.mark.parametrize("name", ["张伟", "Maria", "Ahmed"])
def test_inv_name_does_not_change_intent(clf, name):
    assert clf(f"{name}想查一下快递到哪了") == "track_order"

def test_dir_more_negative_lowers_score(sentiment):
    base = sentiment("物流有点慢")
    assert sentiment("物流有点慢，而且东西坏了，太差了") < base

def test_inv_llm_paraphrase(llm_judge_same):
    a = ask("退货期限是几天？", temperature=0)
    b = ask("买了东西多少天内可以退？", temperature=0)
    assert llm_judge_same(a, b)       # 评委模型判断两个回答事实一致
```

**通过标准：** 最低能力测试要求接近 100%；不变性和方向性测试按失败率设阈值（例如不变性失败率小于 2%），因为模型本来就不完美。

**大语言模型的常见行为测试：**
- **格式：** 要求输出 JSON 时，100 次里 100 次都能被解析。
- **拒答边界：** 明显正常的请求不能被拒；明显违规的请求必须拒。
- **停止：** 回答在合理长度内结束，不会因模板问题一直生成到上限。

**价值：** 一次失败直接告诉你"模型对人名有偏见"或"同义改写会让它改变答案"，比总分下降 0.5 分有用得多；每发现一个线上缺陷，就把它变成一条新的行为测试。
