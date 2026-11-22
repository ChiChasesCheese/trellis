---
id: aie-prompt-versioning-catalog
node: t08.prompt-versioning
type: qa
step: 1
tags: [实践]
---
## Q
**Prompt versioning · 提示词像代码一样管**｜实践 · 必会

线上客服机器人的回答突然变了。有人说「上周三有同事改过 prompt」，但没人记得改了什么。怎么避免这种事？

## A
**第一步：把 prompt 和代码分开存放。** 好处：

| 好处 | 说明 |
|---|---|
| reusability | 多个应用复用同一个 prompt |
| testing | 代码和 prompt 可以分别测试 |
| readability | 两边都更好读 |
| collaboration | 领域专家可以改 prompt，不用碰代码 |

**第二步：给每个 prompt 带元数据**，如模型名、创建时间、应用、创建者；还可包含模型 endpoint、推荐的采样参数（temperature、top-p）、输入 schema、期望的输出 schema。也有专门的 `.prompt` 文件格式（如 Firebase Dotprompt）。

**第三步：版本管理有两种选择：**

| 方式 | 优点 | 缺点 |
|---|---|---|
| prompt 和代码一起放 git | 简单，可回滚 | 多个应用共用同一个 prompt 时，更新会**强制**所有应用升级，没法让某个应用留在旧版 |
| 独立的 **prompt catalog** | 每个 prompt 有显式版本，不同应用用不同版本；可搜索；可记录谁依赖它，并在新版发布时通知负责人 | 要多维护一个系统 |

**发布流程：** 改 prompt → 跑回归评测 → 灰度（canary：先让一小部分真实流量用新版，见发布那组卡）→ 全量；每次请求的 trace 里记录 **prompt 版本号**，这样指标变化可以对应到某次变更。回滚就是把线上指针指回上一个版本。

**检测未经授权的变更：** system prompt 可能因为模板更新、同事改了一个错字而在你不知道的情况下变了；用简单的哈希比较就能发现。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch5 §Organize and Version Prompts；ch10 §Drift detection（System prompt changes）

</details>
