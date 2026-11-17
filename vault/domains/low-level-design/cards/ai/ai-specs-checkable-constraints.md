---
id: ai-specs-checkable-constraints
node: ai.specs
type: qa
step: 5
---
## Q
指令里写了“不许改公开签名、不许改测试”。智能体说它遵守了。有什么办法不靠它的自述，也能确认？

## A
**约束写成能机械检查的形式**

- **签名**：把合同里的签名记成字符串，用 `inspect.signature` 比较，任何改动都立刻看得见；
- **测试文件**：记下它的哈希值，改动前后对一下；
- **可改范围**：只允许修改的文件列在指令里，其他文件的差异就是警报；
- **为什么**：约束只靠口头说，违反了没人发现；写成检查，也方便每一轮都跑。

```python
import hashlib, inspect

def reserve(user_id: str, slot: int, *, now=None): ...

CONTRACT = "(user_id: str, slot: int, *, now=None)"
signature_ok = str(inspect.signature(reserve)) == CONTRACT

test_src = "def test_x():\n    assert reserve('u', 1) is None\n"
digest = lambda s: hashlib.sha256(s.encode()).hexdigest()[:8]
pinned = digest(test_src)
tampered = test_src.replace("None", "1")      # 有人悄悄改了期望值
print(signature_ok, digest(tampered) == pinned)     # True False：测试被改过
```

**知识点：**写清任务（Specifying the Task）
