---
id: hl-j15-strip-trim
node: java21.j15-math-string-utils
type: qa
step: 15
---
## Q
`strip()` 与 `trim()` 有什么区别？`isBlank` 与 `isEmpty`、`lines()` 呢？

## A
- `strip()`（Java 11）按 **Unicode 空白**去；`trim()` 只去 ≤ U+0020 的字符，所以去不掉全角空格（`[　hi]` 里的全角空格还留着）。
- `isBlank()`：全是空白（或空）为 true；`isEmpty()`：长度为 0 才为 true，所以 `"  ".isBlank()` 为 true、`isEmpty()` 为 false。
- `lines()`：按行切成流，同时处理 `\n` 和 `\r\n`。
- `String.repeat(int)`（Java 11）。
