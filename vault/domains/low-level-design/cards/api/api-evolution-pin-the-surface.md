---
id: api-evolution-pin-the-surface
node: api.evolution
type: qa
step: 3
---
## Q
团队约定“公开函数的签名和响应字段不能动”，但约定靠评审时有人记得。怎样让它变成测试，一改就红？

## A
**把对外承诺写成测试，改动必须同时改测试**

- **签名测试**：`inspect.signature(fn)` 与记下的字符串比较；改了参数名、顺序、默认值，测试失败，作者必须有意识地更新；
- **响应键测试**：断言 `result.keys() == {...}`，不是“包含”，多出来的内部字段也会被发现；
- **已发布的迁移同理**：已应用过的迁移文件不许修改，要变化就新增一个；测试可以对文件做哈希；
- **改测试需要理由**：评审时看到测试被改，就知道这是一次对外变更，该走弃用流程；
- **范围**：只钉住公开面，私有函数随便改。

```python
import inspect

def recommend(user: str, *, limit: int = 10) -> list[dict]:
    return [{"id": 1, "title": "t", "score": 0.9, "popularity": 3}]

def test_public_surface():
    assert str(inspect.signature(recommend)) == "(user: str, *, limit: int = 10) -> list[dict]"
    assert recommend("a")[0].keys() == {"id", "title", "score", "popularity"}

test_public_surface()
print("surface unchanged")
```

**知识点：**接口演进（API Evolution）
