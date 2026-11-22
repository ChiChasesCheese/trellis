---
id: aie-silent-model-change-response
node: t08.provider-incident-silent-model-change
type: qa
step: 1
tags: [实践]
---
## Q
**Silent model change · 供应商悄悄换了模型**｜实践 · 必会

某天起，你的抽取任务准确率掉了 10 个点，代码和 prompt 都没改，供应商的状态页一片绿。怎么确认是模型变了，以后怎么防？

## A
**这种事真实发生过：** Chen 等（2023）发现 GPT-3.5 和 GPT-4 在 2023 年 3 月与 6 月两个版本的 benchmark 得分有明显变化；Voiceflow 报告从 GPT-3.5-turbo-0301 换到 1106 后性能下降 10%。供应商不一定提前公告更新。

**确认：**
1. 先排除自己这边的变化：system prompt 有没有被模板改动（比较哈希）、检索数据、用户行为（如用户学会了要求更简洁）；
2. 用**对照回放**：把一批历史请求原样重发给当前模型，并和当时的输出对比，在固定评测集上重新打分；
3. 对比多个指标（长度、拒答率、格式错误率）找出变化的类型。

**预防：**

| 办法 | 做法 |
|---|---|
| **固定模型快照** | 用带日期的版本号，而不是「latest」别名；升级是你主动做的决定 |
| **回归评测** | 每天或每次部署定时跑小型评测集，掉出阈值就报警 |
| **canary**（先分一小部分流量给新模型） | 与旧版对比；另可用 **shadow traffic**（把请求复制给新模型但不返回用户）做对照；细节见发布那组卡 |
| **备用路径** | gateway 配置备用模型，并评测过它 |
| 记录 | 每次请求的 trace 里记下 model 版本 |

**局限：** 开源模型可以完全冻结；商业模型只能靠快照加监控。受强监管的应用对此尤其敏感。

**出处：** Huyen《AI Engineering》ch4 §Are OpenAI's Models Getting Worse?；ch10 §Drift detection（Underlying model changes）；§Gateway（fallback）
