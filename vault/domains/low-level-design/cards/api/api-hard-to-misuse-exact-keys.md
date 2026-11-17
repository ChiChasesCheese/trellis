---
id: api-hard-to-misuse-exact-keys
node: api.hard-to-misuse
type: qa
step: 1
---
## Q
创建工单的接口接受 `{"title": ..., "description": ...}`。调用方把 `description` 拼成了 `desciption`，服务照常返回 201。为什么这是接口设计的问题？该怎么改？

## A
**拼错的键要当场报错，不能悄悄忽略**

- **静默忽略的代价**：请求“成功”了，数据却少了一块；错误在几天后才被人发现，那时已找不到原因；
- **键恰好等于允许集合**：多一个键、少一个必填键，都是 400；每个入口各有自己的允许集合（创建只许这两个，更新只许另外几个）；
- **错误里指出是哪个键**：`unknown_field`，调用方一眼看到拼错的是谁；
- **要兼容旧调用方、容忍未知字段时，是另一个明确的选择**：合同里写“忽略未知字段”，而不是实现碰巧忽略；
- **测试**：加一个多余的键，断言 400；很多实现只测“缺键”，没测“多键”。

```python
ALLOWED = {"title", "description"}

def create_issue(payload: dict) -> dict:
    extra = set(payload) - ALLOWED
    if extra:
        raise ValueError(f"unknown_field: {sorted(extra)}")
    if "title" not in payload:
        raise ValueError("missing_field: title")
    return {"title": payload["title"], "description": payload.get("description", "")}

try: create_issue({"title": "t", "desciption": "x"})
except ValueError as e: print(e)
```

<details class="pt"><summary>延伸</summary>

同样的道理用在函数参数上：位置和名字能由解释器检查的，就别塞进一个 `**kwargs` 里再自己解析；`**kwargs` 吞掉的拼写错误，Python 不会替你提醒。

</details>

**知识点：**难以用错的接口（Hard to Misuse）
