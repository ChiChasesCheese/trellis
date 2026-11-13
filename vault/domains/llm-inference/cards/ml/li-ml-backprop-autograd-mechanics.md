---
id: li-ml-backprop-autograd-mechanics
node: ml.backprop
type: qa
step: 3
---
## Q
PyTorch 的自动求导（autograd）在背后做了什么？为什么每步训练都要调用 `optimizer.zero_grad()`？

## A
**计算图：** 当张量设置了 `requires_grad=True`（参数默认如此），每做一次运算，PyTorch 都在后台记下"这个结果是由哪些输入、经过什么运算得到的"，连成一张有向图。同时保存反向计算要用的中间值，比如乘法要记住两个乘数。

**`loss.backward()`：** 从损失出发，沿着这张图倒着走，对每个节点套用链式法则，把梯度累加到每个参数的 `.grad` 属性上。走完后图被释放。

**标准训练循环：**

```python
for x, y in loader:
    optimizer.zero_grad()          # 清空上一步留下的梯度
    loss = loss_fn(model(x), y)    # 前向：建图并保存中间值
    loss.backward()                # 反向：算梯度，累加进 .grad
    optimizer.step()               # 按梯度更新参数
```

**为什么要 `zero_grad()`：** `.grad` 是**累加**而不是覆盖。不清零，第二步的梯度会加上第一步的，相当于学习率越来越大，训练很快发散。累加的设计是为了支持"梯度累积"：故意连续几个小批量不清零，凑成一个大批量再更新。

**常见坑：**
- **评估或推理时忘了关梯度：** 不用 `torch.no_grad()` 或 `torch.inference_mode()`，PyTorch 仍会建图、存中间值，显存暴涨。
- **把带图的张量存进列表：** 比如 `losses.append(loss)` 而不是 `loss.item()`，整张图都无法释放，显存随步数线性增长，看起来像内存泄漏。
- **原地修改需要的中间值：** 报错 "one of the variables needed for gradient computation has been modified by an inplace operation"。

**和推理的关系：** 推理引擎完全不建计算图，这也是同一个模型推理时显存远小于训练的原因之一。
