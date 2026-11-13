---
id: li-ml-building-blocks-spoken-norm-residual
node: ml.building-blocks
type: qa
step: 4
---
## Q
面试里被问"为什么 Transformer 用 LayerNorm 而不是 BatchNorm？残差连接起什么作用？"，怎么答？

## A
按这个顺序说：

- **先说归一化的目的：** 把每层输入的数值缩放到稳定范围，均值 0、方差 1，再乘加可学习参数，让深网络训练稳定、可以用更大的学习率。
- **两者的唯一区别是统计方向：** BatchNorm 对每个特征沿批里的多个样本求均值方差；LayerNorm 对每个样本沿它自己的特征求。所以 BatchNorm 的结果依赖同批的其他样本，LayerNorm 只依赖样本自己。
- **为什么 Transformer 选 LayerNorm：** 文本长度不一，补齐位置会污染批统计；批小时 BatchNorm 的统计量不稳；BatchNorm 训练和推理用的统计量不同，要维护滑动平均。LayerNorm 训练和推理完全一样，每个 token 独立计算。现代大模型多用 RMSNorm，去掉减均值这一步，更省，效果相当。
- **推理服务的角度（加分）：** 服务会把不同用户的请求动态拼成一批。用 LayerNorm，一个用户的输出不受同批其他人影响，这是推理结果可复现的前提之一。
- **残差连接：** 每个子层的输出加回它的输入，`h = h + f(h)`。反向传播时梯度有一条直通路径，导数里始终有一项 1，几十上百层也不会梯度消失；每层只需学一个修正量，训练更容易。
- **两者的位置：** 现代模型用 pre-norm，先归一化再进注意力或前馈网络，再加回残差；原始 Transformer 是 post-norm，加完残差再归一化，深层时更难训练，需要更仔细的学习率预热。
