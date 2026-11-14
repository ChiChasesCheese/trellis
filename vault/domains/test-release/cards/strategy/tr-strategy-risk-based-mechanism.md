---
id: tr-strategy-risk-based-mechanism
node: strategy.risk-based
type: qa
step: 1
---
## Q
风险驱动测试（risk-based testing）具体怎么做？风险分数怎么算、怎么转化成测试投入？

## A
核心是**把有限的测试时间按风险分配**，而不是平均分给每个功能。

**步骤**：
1. **列出风险项**：按功能、组件或改动列出"可能出错的地方"，例如"新写的矩阵乘法 kernel（kernel：在加速芯片上执行的一小段底层计算代码）在大尺寸输入下数值溢出"。
2. **评估可能性（likelihood）**，1–5 分。依据：改动的大小和复杂度、代码是否新写、该模块历史缺陷密度、作者对模块的熟悉程度、依赖是否变化。
3. **评估影响（impact）**，1–5 分。依据：用户可见程度、是否静默错误（输出错了但不报错最严重）、受影响用户比例、是否可回滚。
4. **风险分数 = 可能性 × 影响**，范围 1–25，排序。
5. **按分数定测试深度**：例如 ≥ 15 分做全组合测试、故障注入和长稳；8–14 分做主路径加边界；≤ 7 分只跑已有回归或明确不测。
6. **写下不测的项和理由**，让风险接受方签字确认。
7. **随结果更新**：测试中发现缺陷集中的模块，可能性分数上调，追加测试。

风险分数落在 5×5 的矩阵上，颜色越深测得越深：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 310">
<g font-family="sans-serif" font-size="12" fill="currentColor">
<g stroke="currentColor" stroke-width="0.8">
<path fill-opacity="0.45" d="M158,14h40v30h-40zM198,14h40v30h-40zM238,14h40v30h-40zM198,44h40v30h-40zM238,44h40v30h-40zM238,74h40v30h-40z"/>
<path fill-opacity="0.18" d="M118,14h40v30h-40zM118,44h40v30h-40zM158,44h40v30h-40zM158,74h40v30h-40zM198,74h40v30h-40zM198,104h40v30h-40zM238,104h40v30h-40z"/>
<path fill-opacity="0.03" d="M78,14h40v30h-40zM78,44h40v30h-40zM78,74h40v30h-40zM118,74h40v30h-40zM78,104h40v30h-40zM118,104h40v30h-40zM158,104h40v30h-40zM78,134h40v30h-40zM118,134h40v30h-40zM158,134h40v30h-40zM198,134h40v30h-40zM238,134h40v30h-40z"/>
</g>
<path fill="none" stroke="currentColor" stroke-width="2.5" d="M200,16h36v26h-36zM160,136h36v26h-36z"/>
<g text-anchor="middle">
<text x="98" y="33">5</text>
<text x="138" y="33">10</text>
<text x="178" y="33">15</text>
<text x="218" y="33">20</text>
<text x="258" y="33">25</text>
<text x="98" y="63">4</text>
<text x="138" y="63">8</text>
<text x="178" y="63">12</text>
<text x="218" y="63">16</text>
<text x="258" y="63">20</text>
<text x="98" y="93">3</text>
<text x="138" y="93">6</text>
<text x="178" y="93">9</text>
<text x="218" y="93">12</text>
<text x="258" y="93">15</text>
<text x="98" y="123">2</text>
<text x="138" y="123">4</text>
<text x="178" y="123">6</text>
<text x="218" y="123">8</text>
<text x="258" y="123">10</text>
<text x="98" y="153">1</text>
<text x="138" y="153">2</text>
<text x="178" y="153">3</text>
<text x="218" y="153">4</text>
<text x="258" y="153">5</text>
<text x="68" y="33">5</text>
<text x="68" y="63">4</text>
<text x="68" y="93">3</text>
<text x="68" y="123">2</text>
<text x="68" y="153">1</text>
<text x="98" y="180">1</text>
<text x="138" y="180">2</text>
<text x="178" y="180">3</text>
<text x="218" y="180">4</text>
<text x="258" y="180">5</text>
<text x="178" y="198">可能性 likelihood</text>
<text x="22" y="89" transform="rotate(-90 22 89)">影响 impact</text>
</g>
<path fill-opacity="0.45" stroke="currentColor" stroke-width="0.8" d="M40,214h16v14h-16z"/>
<text x="64" y="226">≥15 全组合+故障注入+长稳</text>
<path fill-opacity="0.18" stroke="currentColor" stroke-width="0.8" d="M40,236h16v14h-16z"/>
<text x="64" y="248">8–14 主路径+边界</text>
<path fill-opacity="0.03" stroke="currentColor" stroke-width="0.8" d="M40,258h16v14h-16z"/>
<text x="64" y="270">≤7 已有回归或不测</text>
<text x="40" y="298">粗框：新kernel 4×5=20，日志格式 3×1=3</text>
</g>
</svg>
```

**例**：同一版本里，"新 kernel 算错数"可能性 4、影响 5（静默错误：结果错了但不报错），得 20；"日志格式调整"可能性 3、影响 1，得 3。前者分配大部分硬件时间，后者只看冒烟。

打分本身不精确，价值在于**强迫团队把取舍说出来并留下记录**。
