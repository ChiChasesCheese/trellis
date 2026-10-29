---
id: uth-ai-autograd-3-saved-tensors
node: ai.autograd
type: qa
step: 3
---
## Q
**为什么训练比推理吃显存**｜PyTorch · 2.14

同一个模型，训练时的显存为什么比推理多得多？`backward()` 之后 `.grad` 又为什么会越积越多？

## A
**结构。** 有些运算的反向要用前向的中间值：`x²` 的导数是 `2x`，所以前向必须把 `x` 存进节点（saved tensors）。深层网络每一层的输入都被存着，一直留到那一层的反向节点执行完。推理时（`torch.no_grad()` 下）不记图，中间值用完就丢。

**细节。**

- `backward()` 默认走完就释放图和保存的张量（`retain_graph=False`）；对同一个图再调一次会报错，要重复反向就得传 `retain_graph=True`
- 只有叶子张量（`requires_grad=True` 的参数）才存 `.grad`，并且是累加，不是覆盖

```python
x = torch.tensor(3.0, requires_grad=True)
(x * x).backward(); print(x.grad)   # tensor(6.)
(x * x).backward(); print(x.grad)   # tensor(12.)，加在了上一次的 6 上
```

**为什么。** 把前向的中间值存下来，反向时直接取用，不用再重算一遍前向；代价是显存，层数和批量越大，存得越多。

**坑。** 训练循环里每步前要清零梯度（`optimizer.zero_grad()`），否则上一批的梯度还留着，新梯度会加在它上面。

**对应 LeetCode：** 无直接对应的题
