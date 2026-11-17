---
id: reading-char-protect-what-works
node: reading.characterization
type: qa
step: 3
---
## Q
内容审核服务有个缺陷：文本在交给审核器之前被转成了小写，所以“全大写喊叫”永远识别不出来。动手修之前，为什么还要先给“已经正确的部分”写测试？

## A
**修缺陷前，先把没坏的行为钉住，防止“修一个、坏一个”**

- **缺陷旁边常有别的正确行为依赖同一行代码**：这里屏蔽词匹配本来就不分大小写，是对的；
- **看起来顺手的修法会破坏它**：把整个函数里的 `lower()` 都删掉，大写喊叫识别了，屏蔽词却漏掉了 `SPAM`；
- **先写“对的部分”的测试**：它们在修之前就是绿的；修完仍然是绿，才说明你没误伤；
- **再写一条针对缺陷的测试**：修之前红，修之后绿；
- **精确地改**：缺陷在“交给审核器前转了小写”，所以只改这一处，让审核器拿到原文，由它自己决定怎么比较。

```python
BANNED = {"spam"}

def classify(text):                    # 审核器：自己负责大小写
    return {"shout": text.isupper(), "banned": any(w in text.lower() for w in BANNED)}

def moderate(text):
    return classify(text.lower())      # 缺陷：先转小写再交出去

def moderate_fixed(text):
    return classify(text)              # 只改这一处

for f in (moderate, moderate_fixed):
    print(f.__name__, f("BUY SPAM NOW"), f("buy spam now"))
# moderate        shout 对大写永远 False；banned 两种都是 True（已经正确，要保住）
# moderate_fixed  shout 对大写 True；banned 仍然两种都是 True
```

**知识点：**特征测试（Characterization Tests）
