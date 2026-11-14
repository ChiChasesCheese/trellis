---
slug: amazon-ai-repository-debugging
---
## Q
**限时修复 CRUD 仓库（AI 辅助 OA）**｜Medium

给一个带测试的小型 Web 仓库（Django、Spring Boot 或 Node），约 6 个测试失败，可以用 AI 工具，限时修好。缺陷多在路由、状态码、空值和部分更新。

## A
**一句话。** 先跑全量测试定基线，顺着第一个失败的调用路径 route → service → repository 找根因，只改能解释它的那一处，跑定向测试再跑全量；下面是修好后的 service 层该有的样子。

```python
class ItemService:
    def __init__(self):
        self.items, self.next_id = {}, 1

    def create(self, data):
        item = {**data, "id": self.next_id}
        self.items[item["id"]] = item   # 真的存下来
        self.next_id += 1
        return 201, item

    def get(self, item_id):
        item = self.items.get(int(item_id))  # 路径参数是串
        return (200, item) if item else (404, None)

    def patch(self, item_id, data):
        item = self.items.get(int(item_id))
        if item is None:
            return 404, None
        for k, v in data.items():   # 只改传了的字段
            if k != "id":
                item[k] = v
        return 200, item

    def delete(self, item_id):
        self.items.pop(int(item_id), None)  # 幂等
        return 204, None
```

**复杂度。** 时间每个操作 `O(1)`，空间 `O(条目数)`。

**易错点。**
- 部分更新用新对象整体替换：没传的字段被清空，测试读回时变成 `null`。
- 查不到返回 `200` 加 `null`：测试期望 `404`；路径参数是字符串，不转 `int` 永远查不到。
- 让 AI「把测试全修好」：它会改测试或无关契约；每次只给一个失败输出、相关文件和改动边界，最后自己读 diff。

**追问。**
- 第一个失败怎么定位？：先读断言的期望与实际（状态码、字段名、URL 前缀），从路由表找到 handler，再一路跟到存储层。
- 怎么证明没改坏别的？：跑全量测试，再看 `git diff` 只碰了解释失败的那几行。

**同模式。** LC 706 设计哈希映射、LC 1166 设计文件系统、LC 981 基于时间的键值存储
