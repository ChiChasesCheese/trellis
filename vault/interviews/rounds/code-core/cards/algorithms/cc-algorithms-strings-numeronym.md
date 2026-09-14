---
id: cc-algorithms-strings-numeronym
node: algorithms.strings
type: cloze
---
A numeronym keeps a word's first and last character and replaces the middle with its length: `internationalization` becomes {{c1::i18n}}, computed as {{c2::`s[0] + str(len(s) - 2) + s[-1]`}}. It is not always shorter — a 3-letter word becomes {{c3::`x1x`}}, the same length, and a 2-letter word would become {{c4::longer}} — so a real spec gates it with a minimum length, and that boundary is the graded case: a word of exactly `min_len` {{c5::is compressed}} while one character below it is left alone.

## zh
numeronym 保留单词的首尾字符，把中间替换成中间部分的长度：`internationalization` 变成 {{c1::i18n}}，用 {{c2::`s[0] + str(len(s) - 2) + s[-1]`}} 计算。它并不总是更短 —— 3 个字母的单词变成 {{c3::`x1x`}}，长度不变，而 2 个字母的单词会变得 {{c4::更长}} —— 所以真实的 spec 会用最小长度来把关，而那个边界正是会被判分的用例：长度恰为 `min_len` 的单词 {{c5::要被压缩}}，比它少一个字符的则原样保留。
