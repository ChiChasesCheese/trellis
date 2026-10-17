"""LC 68 Text Justification -- greedy line packing, then distribute the slack; last line (and 1-word lines) left-justified."""
from random import Random

# --- solution ---
def full_justify(words, max_width):
    lines, i, n = [], 0, len(words)
    while i < n:
        j, used = i, len(words[i])                     # words[i..j] fit; `used` counts letters plus single spaces
        while j + 1 < n and used + 1 + len(words[j + 1]) <= max_width:
            j += 1
            used += 1 + len(words[j])
        group = words[i:j + 1]
        if j == n - 1 or len(group) == 1:              # last line, or a line that has no gap to stretch
            line = " ".join(group)
            line += " " * (max_width - len(line))
        else:
            slack = max_width - sum(len(w) for w in group)
            gaps = len(group) - 1
            each, extra = divmod(slack, gaps)          # the LEFTMOST `extra` gaps get one more space
            line = "".join(w + " " * (each + (1 if k < extra else 0)) for k, w in enumerate(group[:-1])) + group[-1]
        lines.append(line)
        i = j + 1
    return lines
# --- end ---

def _check(words, width, lines):
    # words survive in order and each line has exactly `width` characters
    assert [w for line in lines for w in line.split()] == words
    assert all(len(line) == width for line in lines)
    k = 0
    for idx, line in enumerate(lines):
        group = line.split()
        # greedy-maximal: the next word would not have fit on this line (with single spaces)
        if idx < len(lines) - 1:
            nxt = words[k + len(group)]
            assert len(" ".join(group)) + 1 + len(nxt) > width
        k += len(group)
        if idx == len(lines) - 1 or len(group) == 1:
            assert line == " ".join(group) + " " * (width - len(" ".join(group)))
        else:
            spaces = []
            pos = 0
            for w in group[:-1]:
                pos = line.index(w, pos) + len(w)
                end = pos
                while line[end] == " ":
                    end += 1
                spaces.append(end - pos)
                pos = end
            assert max(spaces) - min(spaces) <= 1 and spaces == sorted(spaces, reverse=True)

if __name__ == "__main__":
    w = ["This", "is", "an", "example", "of", "text", "justification."]
    assert full_justify(w, 16) == ["This    is    an", "example  of text", "justification.  "]
    w = ["What", "must", "be", "acknowledgment", "shall", "be"]
    assert full_justify(w, 16) == ["What   must   be", "acknowledgment  ", "shall be        "]
    w = ["Science", "is", "what", "we", "understand", "well", "enough", "to", "explain", "to", "a", "computer.",
         "Art", "is", "everything", "else", "we", "do"]
    assert full_justify(w, 20) == ["Science  is  what we", "understand      well", "enough to explain to", "a  computer.  Art is",
                                   "everything  else  we", "do                  "]
    assert full_justify(["a"], 1) == ["a"]
    rng = Random(97)
    for _ in range(400):
        width = rng.randint(4, 14)
        words = ["x" * rng.randint(1, width) for _ in range(rng.randint(1, 12))]
        _check(words, width, full_justify(words, width))
    print("ok 68_text_justification")
