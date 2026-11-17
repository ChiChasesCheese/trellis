---
id: data-defensive-copy-snapshot-iterable
node: data.defensive-copy
type: qa
step: 5
---
## Q
服务接受 `Iterable[str]` 的黑名单关键词。调用方传进来的是生成器，或者传进来的是列表但稍后又被他修改。服务先遍历校验一遍、之后再用，会出什么问题？

## A
**先读成快照，再校验、再使用同一份**

- **生成器只能遍历一次**：校验循环把它耗尽，后面的使用拿到的是空；没有任何报错，黑名单悄悄失效；
- **检查与使用之间的空隙**：列表在校验之后、使用之前被改，校验过的和用到的就不是同一份（先检查后使用，TOCTOU）；
- **做法**：入口第一行 `words = tuple(words)`，之后只碰 `words`；
- **选元组**：快照本身也不可变，以后的方法不会在里面改；
- **这是合同的一部分**：文档写“接受任意可迭代对象，调用时读取一次”，调用方就知道之后改原容器无效。

```python
def block_words(words):
    snapshot = tuple(words)                       # 先读成快照，只遍历这一次
    if not all(isinstance(w, str) and w for w in snapshot):
        raise ValueError("invalid_keywords")
    return lambda text: any(w in text for w in snapshot)

src = ["spam"]
match = block_words(w for w in src)               # 生成器
src.append("scam")
print(match("a spam"), match("a scam"))           # True False
```

**知识点：**防御性拷贝（Defensive Copying）
