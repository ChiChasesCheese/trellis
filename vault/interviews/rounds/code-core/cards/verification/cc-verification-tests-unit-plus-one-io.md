---
id: cc-verification-tests-unit-plus-one-io
node: verification.tests
type: qa
---
## Q
All your tests call `part3(rows)` directly and pass. What class of failure is still invisible, and what single extra test closes it?

## A
**Everything between stdin and that function**: header parsing, part dispatch, the trailing newline, a stray debug line, `print` versus `write`.

- Add exactly **one** end-to-end test that feeds a sample through `main` with `io.StringIO` and compares the whole stdout string, byte for byte ([[cc-python-io-main-seam]]).
- Unit tests give fast, precise failures; the single I/O test proves the wiring. You need both, and only one of the second kind.
- Compare with `==` on the entire string, never line by line — that is exactly what catches a missing or extra terminal newline, and a blank line where the answer is empty.

## Q zh
你的测试全都直接调 `part3(rows)` 并且都通过。哪一类失败仍然不可见？加哪一个测试就能堵住它？

## A zh
**stdin 与那个函数之间的一切**：表头解析、part 分派、结尾换行、残留的调试行、`print` 与 `write` 之别。

- 恰好加**一个**端到端测试：用 `io.StringIO` 把样例喂给 `main`，逐字节比对整个 stdout 字符串（[[cc-python-io-main-seam]]）。
- 单元测试给你快速而精确的失败；那一个 I/O 测试证明接线正确。两者都要，而第二种只要一个。
- 用 `==` 比对整个字符串，绝不逐行比 —— 这正是抓住「少了或多了一个结尾换行」以及「答案为空却打了空行」的办法。
