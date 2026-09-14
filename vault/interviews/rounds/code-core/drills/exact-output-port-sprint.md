---
nodes: [output.formatting, output.sentinels, python.io, python.idioms, verification.tests]
---
# Drill: twenty minutes to an exact-output contract

Twenty minutes, timed strictly. You are given a working function that returns a
list of records and a written output contract:

- one line per record, `<id> | <name padded to 12 columns> | $<amount, two decimals, thousands separators> | <status upper-cased>`
- records sorted by amount descending, then id ascending
- a header line, and a trailing summary line `TOTAL | $<sum>`
- when there are no records, print the literal `NO RECORDS` and nothing else

Write only the rendering layer, plus tests that prove it. The point of the drill
is that the logic is already correct and you can still fail every hidden test.

**Constraints to state and honor**
- The whole stdout string is compared byte for byte, including the final newline.
- Amounts arrive as integer minor units; the formatter is the only place they
  become a decimal string.
- No debug output on stdout.

**Grading points**
- One formatting function, called once per record, with the padding and the
  separators in the format spec rather than in string concatenation
  ([[cc-python-idioms-fstring-format]]).
- The empty case produces `NO RECORDS` with no header and no blank line
  ([[cc-python-io-exact-stdout]]).
- Trailing newline present exactly once; test it with `==` on the whole string
  ([[cc-verification-tests-unit-plus-one-io]]).
- Descending-then-ascending order achieved without `reverse=True` on a mixed key
  ([[cc-python-idioms-sorted-key-mechanics]]).
- A record with a name longer than 12 columns, an amount of zero, and an amount
  over 1,000,000 ([[cc-verification-edge-zero-negative-and-max]]).

**Attempt log**
- [ ] Attempt 1 (date, 20 min, self-graded notes):
