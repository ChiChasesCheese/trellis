---
id: cc-input-norm-key-canonical-print-original
node: input.normalization
type: qa
---
## Q
A request header says `EN-us`; the server's supported list says `en-US`. Which spelling appears in your output?

## A
**Compare on the canonical form, print the spelling that owns the value — here the supported list's `en-US`.**

The pattern is a dict from canonical key to the original token: `{"en-us": "en-US"}`. Matching goes through the key, output goes through the value.

Which side "owns" the spelling is stated by the problem and is worth reading twice: a language tag is printed as the *server* spells it, a company name may be printed as the *registrant* typed it, a merchant id is usually echoed exactly as it arrived. Lower-casing your output is a byte-exactness failure, not a normalization.

## Q zh
请求头写的是 `EN-us`；服务端支持列表里写的是 `en-US`。输出里出现哪种拼写？

## A zh
**用规范形式比较，用拥有该值的一方的拼写来打印 —— 这里是支持列表的 `en-US`。**

模式是一个"规范 key → 原始 token"的 dict：`{"en-us": "en-US"}`。匹配走 key，输出走 value。

拼写归谁"所有"由题面规定，值得读两遍：语言标签按**服务端**的写法打印，公司名可能按**注册人**输入的写法打印，商户 id 通常原样回显。把输出统一转小写是字节精确性的失败，不是归一化。
