---
id: leetcode-c-endlesscheng-mdfnkw-modular-inverse-fermat-invariant
node: math-number-theory.modular-inverse-fermat
type: cloze
anki: 1787272451679
tags: [concept-cloze, invariant, leetcode, recall]
---
费马小定理：若 p 是质数且 b 不是 p 的倍数，则 {{c1::b^(p-1) ≡ 1}} (mod p)，因此 b 的逆元为 {{c2::b^(p-2)}} mod p。

费马小定理：对质数 p 和任意整数 b，b^p ≡ b (mod p)；若 b 不是 p 的倍数，则 b^(p-1) ≡ 1 (mod p)；b 的逆元为 b^(p-2) mod p（p 为质数）；(a/b) mod p = (a·b^(p-2)) mod p = (a·inv(b)) mod p

**Evidence**

除法的取模

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.06%20-%20%E8%B4%B9%E9%A9%AC%E5%B0%8F%E5%AE%9A%E7%90%86%E4%B8%8E%E6%A8%A1%E9%80%86%E5%85%83%EF%BC%88%E9%99%A4%E6%B3%95%E5%8F%96%E6%A8%A1%EF%BC%89)
