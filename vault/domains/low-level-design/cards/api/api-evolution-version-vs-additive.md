---
id: api-evolution-version-vs-additive
node: api.evolution
type: qa
step: 4
---
## Q
接口一定要出 `/v2` 吗？什么时候新增版本，什么时候在原接口上增量演进？

## A
**能增量就增量，只有破坏性变更才开新版本**

- **增量演进**：新增可选参数、新增响应字段、放宽输入；老调用方不受影响，不需要新版本；
- **新版本**：返回结构变了、语义变了、字段改名；老调用方还在用，不能强行跟着改；
- **每个版本都是要维护的一份**：两个版本同时存在，修一个 bug 要修两处，测试加倍；所以版本不是免费的；
- **做法**：新旧版本共用同一个内部实现，各自只有一层薄薄的转换（老版本把新结果转成旧形状）；
- **会变的数据**：规则会变的东西（风控阈值、汇率），让版本号成为数据的一部分，请求读哪个版本要事先约定好。

```python
def core(user: str) -> dict:                         # 唯一的实现，用最新形状
    return {"id": 1, "title": "t", "score": 0.9}

def recommend_v1(user: str) -> list[str]:            # 老版本：只是转换
    return [core(user)["title"]]

def recommend_v2(user: str) -> list[dict]:
    return [core(user)]

print(recommend_v1("a"), recommend_v2("a"))
```

<details class="pt"><summary>延伸</summary>

弃用的期限是版本策略的一部分：写明每个旧版本支持多久、最后一个调用方什么时候迁完。没有期限，旧版本会永久留下来，成本不断累积。

</details>

**知识点：**接口演进（API Evolution）
