%% trellis:begin %%
# 分词器：BPE 的贪心合并与 Unigram 的动态规划
*AI 工程里的数据结构与算法*

文本怎样切成 token：BPE（tiktoken 等）反复把优先级最高的相邻一对并成一个（tiktoken 里 token 的编号就是合并优先级）；SentencePiece 的 Unigram 用 Viterbi（动态规划）在所有切法里挑概率最大的，和单词拆分是同一个 DP。

## Cards (4)
1. [[uth-ai-tokenizer-1-bpe-merge]]
2. [[uth-ai-tokenizer-2-pretokenize]]
3. [[uth-ai-tokenizer-3-unigram-viterbi]]
4. [[uth-ai-tokenizer-4-merge-heap]]
%% trellis:end %%

## Notes
