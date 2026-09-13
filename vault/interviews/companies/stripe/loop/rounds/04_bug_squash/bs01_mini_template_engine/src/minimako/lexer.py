"""Line-oriented tokenizer for minimako's template mini-language.

Supported syntax:
  ${expr}                        -- an interpolated Python expression
  % if COND / % endif            -- control line, must be alone on its line
  % for X in ITER / % endfor     -- control line, must be alone on its line
  <%include file="uri"/>         -- render another template inline

Everything else is literal text, reproduced verbatim (including newlines).
"""

from __future__ import annotations

import re

CONTROL_RE = re.compile(r"^\s*%\s*(if|for|endif|endfor)\b(.*)$")
INLINE_RE = re.compile(r'\$\{[^}]*\}|<%include\s+file="[^"]*"\s*/?>')
INCLUDE_RE = re.compile(r'<%include\s+file="([^"]*)"\s*/?>')

# Token = (kind, value). kind in {"text", "expr", "include", "if", "for", "endif", "endfor"}.
Token = tuple[str, str | None]


def tokenize(text: str) -> list[Token]:
    tokens: list[Token] = []
    ends_with_newline = text.endswith("\n")
    lines = text.split("\n")
    if ends_with_newline:
        lines = lines[:-1]  # the trailing "" from split() isn't a real line

    for idx, line in enumerate(lines):
        m = CONTROL_RE.match(line)
        if m:
            kind, rest = m.group(1), m.group(2).strip()
            if kind in ("if", "for"):
                rest = rest.rstrip(":").strip()
                tokens.append((kind, rest))
            else:  # endif / endfor
                tokens.append((kind, None))
            continue

        pos = 0
        for im in INLINE_RE.finditer(line):
            if im.start() > pos:
                tokens.append(("text", line[pos : im.start()]))
            seg = im.group(0)
            if seg.startswith("${"):
                tokens.append(("expr", seg[2:-1].strip()))
            else:
                inc = INCLUDE_RE.match(seg)
                tokens.append(("include", inc.group(1)))
            pos = im.end()
        if pos < len(line):
            tokens.append(("text", line[pos:]))

        is_last_line = idx == len(lines) - 1
        if not (is_last_line and not ends_with_newline):
            tokens.append(("text", "\n"))

    return tokens
