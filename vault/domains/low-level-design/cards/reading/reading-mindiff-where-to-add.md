---
id: reading-mindiff-where-to-add
node: reading.minimal-diff
type: qa
step: 3
---
## Q
导出模块用一张 `EXPORTERS` 表按格式分派，已有 `csv` 和 `json`，现在要加一种 `ndjson`。新功能放在哪里，改动对原来的代码打扰最小？

## A
**优先“添加”，其次才是“修改”：找代码里已经留着的扩展点**

- **已有表驱动**：直接在表里加一行，其余代码一行不动；
- **没有表时**：新增一个独立函数，在分派处加一个分支；不要改已有分支里的逻辑；
- **把新代码放在相关代码旁边**：同一个文件、同一个区域，读的人容易找到；
- **别为了新功能重新组织旧代码**：除非旧结构让新功能做不下去；
- **新增代码要有自己的测试**，已有的测试一条都不用改，改了反而说明碰到了旧行为。

```python
import json

def to_csv(rows): return "\n".join(",".join(map(str, r)) for r in rows)
def to_json(rows): return json.dumps(rows)
def to_ndjson(rows): return "\n".join(json.dumps(r) for r in rows)    # 新增：一个独立函数

EXPORTERS = {"csv": to_csv, "json": to_json,
             "ndjson": to_ndjson}                                       # 新增：表里一行

def export(fmt, rows): return EXPORTERS[fmt](rows)

print(export("ndjson", [[1, 2], [3, 4]]))
```

**知识点：**最小改动（Minimal Diff）
