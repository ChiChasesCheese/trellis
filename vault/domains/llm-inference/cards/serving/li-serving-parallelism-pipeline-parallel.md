---
id: li-serving-parallelism-pipeline-parallel
node: serving.parallelism
type: qa
step: 2
---
## Q
流水线并行（pipeline parallelism，PP）怎样切分模型？为什么它不能降低单个请求的每 token 延迟，却能提高吞吐？

## A
**切法：** 按层切。80 层的模型放 4 张卡（或 4 台机器）：第 1 张放第 1–20 层，第 2 张放 21–40 层，以此类推。每个阶段（stage）算完自己的层，把这一步的中间结果（激活值，每个 token 一个隐藏向量）发给下一个阶段。

**只需传激活值：** 每个 token 在阶段之间只传一个隐藏向量，8,192 维 × 2 字节 = 16 KB。比张量并行每层两次全体求和少得多，所以流水线并行可以跨机器、走较慢的网络。

**为什么单请求不变快：** 生成一个 token 必须依次穿过全部 80 层。不管切成几段，一个 token 的路径都是"阶段 1 → 2 → 3 → 4"，时间 = 各阶段时间之和 + 每次传递的延迟。切得越多，传递次数越多，单请求甚至略慢。而且生成下一个 token 必须等这个 token 走完全程。

**为什么能提高吞吐：** 只有一个请求时，阶段 1 算完就闲着，等阶段 4 算完才有下一个 token 可算。如果同时有多组请求（微批，micro-batch）：
- 时刻 1：阶段 1 算 A 组；
- 时刻 2：阶段 1 算 B 组，阶段 2 算 A 组；
- 时刻 4 之后：4 个阶段同时在算 4 组不同的请求。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 166" font-family="sans-serif" font-size="11">
<text x="84" y="14" text-anchor="end" fill="currentColor">阶段（层）</text>
<text x="90" y="14" fill="currentColor">时刻 →</text>
<text x="107" y="28" text-anchor="middle" fill="currentColor">1</text>
<text x="141" y="28" text-anchor="middle" fill="currentColor">2</text>
<text x="175" y="28" text-anchor="middle" fill="currentColor">3</text>
<text x="209" y="28" text-anchor="middle" fill="currentColor">4</text>
<text x="243" y="28" text-anchor="middle" fill="currentColor">5</text>
<text x="277" y="28" text-anchor="middle" fill="currentColor">6</text>
<text x="311" y="28" text-anchor="middle" fill="currentColor">7</text>
<text x="84" y="51" text-anchor="end" fill="currentColor">1–20 层</text>
<rect x="90" y="36" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="107" y="51" text-anchor="middle" fill="currentColor">A</text>
<rect x="124" y="36" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="141" y="51" text-anchor="middle" fill="currentColor">B</text>
<rect x="158" y="36" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="175" y="51" text-anchor="middle" fill="currentColor">C</text>
<rect x="192" y="36" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="209" y="51" text-anchor="middle" fill="currentColor">D</text>
<rect x="226" y="36" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="243" y="51" text-anchor="middle" fill="currentColor">E</text>
<rect x="260" y="36" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="277" y="51" text-anchor="middle" fill="currentColor">F</text>
<rect x="294" y="36" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="311" y="51" text-anchor="middle" fill="currentColor">G</text>
<text x="84" y="77" text-anchor="end" fill="currentColor">21–40 层</text>
<rect x="90" y="62" width="34" height="22" fill="none" stroke="currentColor" stroke-dasharray="3 2"/>
<rect x="124" y="62" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="141" y="77" text-anchor="middle" fill="currentColor">A</text>
<rect x="158" y="62" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="175" y="77" text-anchor="middle" fill="currentColor">B</text>
<rect x="192" y="62" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="209" y="77" text-anchor="middle" fill="currentColor">C</text>
<rect x="226" y="62" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="243" y="77" text-anchor="middle" fill="currentColor">D</text>
<rect x="260" y="62" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="277" y="77" text-anchor="middle" fill="currentColor">E</text>
<rect x="294" y="62" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="311" y="77" text-anchor="middle" fill="currentColor">F</text>
<text x="84" y="103" text-anchor="end" fill="currentColor">41–60 层</text>
<rect x="90" y="88" width="34" height="22" fill="none" stroke="currentColor" stroke-dasharray="3 2"/>
<rect x="124" y="88" width="34" height="22" fill="none" stroke="currentColor" stroke-dasharray="3 2"/>
<rect x="158" y="88" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="175" y="103" text-anchor="middle" fill="currentColor">A</text>
<rect x="192" y="88" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="209" y="103" text-anchor="middle" fill="currentColor">B</text>
<rect x="226" y="88" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="243" y="103" text-anchor="middle" fill="currentColor">C</text>
<rect x="260" y="88" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="277" y="103" text-anchor="middle" fill="currentColor">D</text>
<rect x="294" y="88" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="311" y="103" text-anchor="middle" fill="currentColor">E</text>
<text x="84" y="129" text-anchor="end" fill="currentColor">61–80 层</text>
<rect x="90" y="114" width="34" height="22" fill="none" stroke="currentColor" stroke-dasharray="3 2"/>
<rect x="124" y="114" width="34" height="22" fill="none" stroke="currentColor" stroke-dasharray="3 2"/>
<rect x="158" y="114" width="34" height="22" fill="none" stroke="currentColor" stroke-dasharray="3 2"/>
<rect x="192" y="114" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="209" y="129" text-anchor="middle" fill="currentColor">A</text>
<rect x="226" y="114" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="243" y="129" text-anchor="middle" fill="currentColor">B</text>
<rect x="260" y="114" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="277" y="129" text-anchor="middle" fill="currentColor">C</text>
<rect x="294" y="114" width="34" height="22" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="311" y="129" text-anchor="middle" fill="currentColor">D</text>
<text x="4" y="160" fill="currentColor">A–G 是不同的请求组；虚线框是空闲的气泡</text>
</svg>

只要在途的组数 ≥ 阶段数，每个阶段都不闲着。**在途请求数 ≈ 阶段数 × 每组大小**。

**气泡（bubble）：** 在途组数不足时，部分阶段空闲。流量低时利用率差；各阶段工作量不均衡时，最慢的阶段决定整条流水线的节奏。

**取舍：**
- 每组越小，单个请求越快（每步等待少），总吞吐越低；
- 每组越大，吞吐越高，单个请求越慢。

**实际组合：** 机器内用张量并行（需要高速互联），机器之间用流水线并行（只传激活值）。
