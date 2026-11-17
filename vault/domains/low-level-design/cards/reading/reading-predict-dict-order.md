---
id: reading-predict-dict-order
node: reading.predict-behaviour
type: qa
step: 3
---
## Q
购物车用字典存商品行，`update_line` 的实现是先 `del cart[sku]` 再 `cart[sku] = new`。改完一个已有商品的数量后，遍历顺序会怎样？换成 `cart[sku] = new` 呢？

## A
**字典保持插入顺序：删除再插入会排到末尾，直接覆盖则原地不动**

- **Python 3.7 起，字典遍历顺序就是键第一次被插入的顺序**（语言规范保证）；
- **`cart[k] = v`，k 已存在**：只替换值，位置不变；
- **`del cart[k]` 再 `cart[k] = v`**：k 被当成新键，追加到末尾；
- **推演时的提示**：看到“先删后设”，就想“位置变了”；展示顺序有意义时（购物车行、收件箱），要明确选一种并写进规格；
- **想让顺序固定**：显式排序（`sorted(cart)`）；或者保证更新走“覆盖”路径。

```python
cart = {"apple": 1, "pear": 2, "fig": 3}

a = dict(cart); a["apple"] = 5
print(list(a))                         # ['apple', 'pear', 'fig']：覆盖，位置不变

b = dict(cart); del b["apple"]; b["apple"] = 5
print(list(b))                         # ['pear', 'fig', 'apple']：先删后设，落在末尾
```

**知识点：**预测输出与副作用（Predicting Behaviour）
