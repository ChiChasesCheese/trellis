#!/usr/bin/env python3
"""Find text diagrams that break on a phone (WRITING_RULES rule 12).

    python3 scripts/phone_diagrams.py <file.md | dir> [...]

A fenced block that is not code (no language, `text`, `plaintext`, …) and draws with box/arrow characters must be
at most 40 display columns wide (a CJK character counts 2) and must not put CJK characters on a line that also
draws (CJK glyphs are not exactly two cells wide, so box edges stop lining up). Exit 1 if anything is reported.
"""
import glob, os, re, sys, unicodedata

CODE = {'python', 'py', 'java', 'cpp', 'c++', 'c', 'bash', 'sh', 'sql', 'json', 'yaml', 'go', 'rust', 'kotlin',
        'javascript', 'js', 'ts', 'typescript', 'mermaid', 'diff', 'toml', 'xml', 'html', 'css', 'console', 'asm'}
DRAW = re.compile(r'[─│┌┐└┘├┤┬┴┼═║╔╗╚╝▶◀▲▼←→↑↓┃━]|\+-{2,}|-{2,}>|<-{2,}|\|.*\|')
MAX = 40


def width(s):
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)


def cjk(s):
    return any(unicodedata.east_asian_width(c) in 'WF' for c in s)


def problems(text):
    out = []
    for m in re.finditer(r'^```([^\n]*)\n(.*?)^```', text, re.S | re.M):
        lang = m.group(1).strip().lower()
        body = m.group(2)
        if lang in CODE or not DRAW.search(body):
            continue
        line = text[:m.start()].count('\n') + 1
        lines = body.split('\n')
        wide = max((width(l) for l in lines), default=0)
        mixed = [l for l in lines if DRAW.search(l) and cjk(l)]
        if wide > MAX:
            out.append(f'line {line}: diagram {wide} columns wide (max {MAX})')
        if mixed:
            out.append(f'line {line}: CJK on a drawing line ({len(mixed)} lines) — move labels to a legend, table or mermaid')
    return out


def files(args):
    for a in args:
        if os.path.isdir(a):
            for f in glob.glob(os.path.join(a, '**', '*.md'), recursive=True):
                if '/examples/out/' not in f and '/demos/' not in f:
                    yield f
        else:
            yield a


def main(args):
    bad = 0
    for f in files(args):
        p = problems(open(f, encoding='utf-8').read())
        if p:
            bad += 1
            print('FAIL', f)
            for x in p:
                print('      -', x)
    print(f'{bad} file(s) fail' if bad else 'ok')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
