---
id: li-ml-classification-metrics-spoken-precision-recall
node: ml.classification-metrics
type: qa
step: 4
---
## Q
面试里被问"精确率和召回率是什么，怎么取舍？举个你会用到的例子"，怎么答？

## A
按这个顺序说：

- **先画混淆矩阵：** 预测和真实交叉成四格：真阳性、假阳性（误报）、假阴性（漏报）、真阴性。所有指标都从这四个数来。
- **两个定义：** 精确率 = TP /（TP + FP），模型报出来的里面有多少是真的；召回率 = TP /（TP + FN），真的里面有多少被报出来了。F1 是两者的调和平均，偏向较低的那个。

<svg viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="13" fill="currentColor" stroke="currentColor">
  <text x="200" y="18" text-anchor="middle" stroke="none">真实</text>
  <text x="150" y="40" text-anchor="middle" stroke="none">阳性</text>
  <text x="250" y="40" text-anchor="middle" stroke="none">阴性</text>
  <text x="18" y="120" text-anchor="middle" stroke="none" transform="rotate(-90 18 120)">预测</text>
  <text x="65" y="85" text-anchor="middle" stroke="none">阳性</text>
  <text x="65" y="155" text-anchor="middle" stroke="none">阴性</text>
  <rect x="100" y="50" width="100" height="70" fill="none"/>
  <rect x="200" y="50" width="100" height="70" fill="none"/>
  <rect x="100" y="120" width="100" height="70" fill="none"/>
  <rect x="200" y="120" width="100" height="70" fill="none"/>
  <text x="150" y="90" text-anchor="middle" stroke="none">TP 真阳性</text>
  <text x="250" y="90" text-anchor="middle" stroke="none">FP 误报</text>
  <text x="150" y="160" text-anchor="middle" stroke="none">FN 漏报</text>
  <text x="250" y="160" text-anchor="middle" stroke="none">TN 真阴性</text>
</svg>

- **为什么不看准确率：** 类别不平衡时会骗人。1% 是阳性的数据，全猜阴性就有 99% 准确率，召回率却是 0。
- **取舍靠阈值和业务成本：** 降低阈值，召回率升、精确率降；反之亦然。漏报代价高的场景（癌症筛查、欺诈、安全过滤）要高召回；误报代价高的场景（自动封号、自动阻断发布）要高精确。需要单一数字时，用 Fβ，β 大于 1 偏向召回。不依赖阈值的排序能力看 ROC-AUC，严重不平衡时看 PR-AUC。
- **举一个测试工程的例子：** 发布流水线里用一个分类器判断"失败的用例是真缺陷还是偶发抖动"，判为抖动的自动重试、不阻断发布。这里把真缺陷当阳性：漏报（真缺陷被当成抖动放过）代价是缺陷上线，远大于误报（抖动被当成缺陷、要人看一眼）的代价，所以我会优先保召回率，比如要求真缺陷召回率 ≥ 99%，在这个约束下尽量提高精确率，减少人工复核量。
- **收尾说怎么评估：** 用最近几个月人工标注过的失败记录做测试集，按时间切分而不是随机切分，每次改阈值或模型都报告混淆矩阵和这两个指标。
