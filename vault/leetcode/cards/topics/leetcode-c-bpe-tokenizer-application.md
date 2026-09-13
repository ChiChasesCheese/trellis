---
id: leetcode-c-bpe-tokenizer-application
node: topics.uncategorised
type: qa
anki: 1787365290831
tags: [algorithm::byte-pair-encoding, algorithm::frequency-counting, algorithm::greedy-merging, algorithm::priority-queue, application, case, case::bpe-tokenizer, category::developer-infrastructure, chapter::08, chapter::10, chapter::12, leetcode, system::hugging-face-tokenizers, system::large-language-models]
---
## Q
BPE 的训练和编码分别做什么？为什么词表越大不一定越好？

## A
训练从基础 symbols 开始，反复统计相邻 pair 并贪心合并最高频 pair，产出 vocabulary 和有优先级的 merge rules；编码只应用固定 rules。大词表通常缩短序列，但扩大 embedding/output matrix、减少稀有 token 样本并增加 artifact 成本。

**Evidence**

Hugging Face 官方 quicktour 明确描述从字符开始、反复合并最高频 pair 直到目标词表大小，官方 API 将 BPE 放在完整 tokenizer pipeline 中。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FBPE%20Tokenizer%EF%BC%9A%E9%A2%91%E7%8E%87%E7%BB%9F%E8%AE%A1%E3%80%81%E8%B4%AA%E5%BF%83%E5%90%88%E5%B9%B6%E4%B8%8E%E8%AF%8D%E8%A1%A8%E6%9D%83%E8%A1%A1)
