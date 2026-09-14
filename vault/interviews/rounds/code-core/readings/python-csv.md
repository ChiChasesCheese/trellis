---
nodes: [python.stdlib, input.delimited, input.malformed]
url: https://docs.python.org/3/library/csv.html
tags: [docs]
---
# csv — CSV file reading and writing

Worth ten minutes because `line.split(",")` is right until one field is quoted
and contains a comma, at which point every column after it shifts and the
failure looks like a logic bug. `csv.reader` handles quoting, embedded
newlines and escapes; `csv.DictReader` gives header-driven access so column
order stops mattering. The page also documents `restkey` and `restval`, which
are how you decide what a short or long row means.

**Extract on read:**
- `DictReader(f)` plus stripping keys and values — column order becomes free.
- `restkey` / `restval` for rows with too many or too few fields
  ([[cc-verification-edge-duplicate-and-out-of-order]]).
- Dialects and `delimiter=`/`quotechar=` for pipe- or tab-separated input, and
  why `newline=""` matters when you open a real file.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/csv.html)

## Archived copy
![[python-csv-clip]]
%% trellis:end %%
