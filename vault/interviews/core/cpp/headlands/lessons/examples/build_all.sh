#!/usr/bin/env bash
# Compile and run every example under study/20-cpp/examples/C*/*.cpp.
#   ./build_all.sh              # all files
#   ./build_all.sh C05          # only files whose path contains C05
# Default flags (kit AGENT_RULES): clang++ -std=c++20 -O2 -Wall -Wextra -fsanitize=address,undefined
# Per-file directives, in the first 25 lines, as "// KEY: value":
#   STD:    language standard override (default c++20)           e.g. "// STD: c++11"
#   SAN:    default | thread | none                              (default: address,undefined)
#   EXTRA:  extra compiler flags                                 e.g. "// EXTRA: -fno-exceptions"
#   EXPECT: ok | warn | compile-fail | run-fail                  (default ok: compiles with no
#           diagnostics, exits 0; warn: compiles with warnings; run-fail: sanitizer/abort expected,
#           warnings allowed)
#   RUN:    shell command, $BIN is the binary (repeatable)       (default "$BIN")
#           SAN: none is for timing benchmarks; the file is ALSO built and run with the default
#           sanitizers (output discarded, must exit 0) so correctness is still checked.
#   ALSO:   thread -> also build and run with ThreadSanitizer; must report nothing (output appended)
#   ASM:    yes  -> also writes out/<name>.s (clang++ -S -O2, no sanitizers)
# Output of each file is stored in out/<name>.txt (paths scrubbed, sanitizer reports cut at SUMMARY).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/out"; BINDIR="${TMPDIR:-/tmp}/cpp20_build"; PATTERN="${1:-}"
mkdir -p "$OUT" "$BINDIR"
CXX="${CXX:-clang++}"
# The macOS symbolizer (atos) can hang inside sandboxes; frames then show raw addresses, the report lines are unchanged.
export ASAN_OPTIONS="${ASAN_OPTIONS:-symbolize=0}" TSAN_OPTIONS="${TSAN_OPTIONS:-symbolize=0}"
run_cmd() { # run a shell command with a 120 s limit
  perl -e 'alarm 120; exec "bash", "-c", $ARGV[0]' "$1"
}
pass=0; fail=0; failed=""

directive() { # file key default
  local v
  v=$(head -25 "$1" | sed -n "s|^// $2: *||p" | head -1)
  if [ -n "$v" ]; then echo "$v"; else echo "$3"; fi
}
scrub() { sed -E -e "s|$HERE/||g" -e "s|$BINDIR/||g" -e 's/\.\/build_all\.sh: line [0-9]+: [0-9]+ (Abort trap|Segmentation fault|Bus error).*//' ; }
# keep everything, but drop the (huge) shadow-byte dump that follows an AddressSanitizer SUMMARY line
cut_asan() { awk '/^SUMMARY:/{seen=1; print; next} !seen{print; next} /^Shadow|^  0x|^=>|^  [A-Za-z ]+: +[0-9a-f][0-9a-f]( |$)|ABORTING/{next} {print}' ; }

for f in "$HERE"/C*/*.cpp; do
  case "$f" in *"$PATTERN"*) ;; *) continue;; esac
  name="$(basename "$f" .cpp)"
  std=$(directive "$f" STD c++20); san=$(directive "$f" SAN default)
  extra=$(directive "$f" EXTRA ""); expect=$(directive "$f" EXPECT ok)
  case "$san" in
    default) sf="-fsanitize=address,undefined";;
    thread)  sf="-fsanitize=thread";;
    none)    sf="";;
  esac
  bin="$BINDIR/$name"; ccout="$BINDIR/$name.cc"; rm -f "$bin"
  # shellcheck disable=SC2086
  (cd "$HERE" && $CXX -std=$std -O2 -Wall -Wextra $sf $extra "$f" -o "$bin") >"$ccout" 2>&1
  cc=$?; ok=1; why=""
  : >"$OUT/$name.txt"
  if [ "$expect" = compile-fail ]; then
    [ $cc -ne 0 ] || { ok=0; why="expected compile failure"; }
    scrub <"$ccout" >"$OUT/$name.txt"
  else
    if [ $cc -ne 0 ]; then ok=0; why="compile failed"; scrub <"$ccout" >"$OUT/$name.txt"; fi
    if [ $ok = 1 ] && [ -s "$ccout" ]; then
      if [ "$expect" = warn ] || [ "$expect" = run-fail ]; then scrub <"$ccout" >"$OUT/$name.cc.txt"; else ok=0; why="compiler diagnostics (expected none)"; scrub <"$ccout" >"$OUT/$name.txt"; fi
    fi
  fi
  if [ $ok = 1 ] && [ "$expect" != compile-fail ]; then
    runs=$(head -25 "$f" | sed -n 's|^// RUN: *||p'); [ -n "$runs" ] || runs='$BIN'
    export BIN="$bin"; rc_all=0
    while IFS= read -r cmd; do
      echo "\$ ${cmd//\$BIN/$name}" >>"$OUT/$name.txt"
      (cd "$HERE/$(basename "$(dirname "$f")")" && run_cmd "$cmd") >"$BINDIR/$name.run" 2>&1
      rc=$?
      if [ "$expect" = run-fail ]; then scrub <"$BINDIR/$name.run" | cut_asan >>"$OUT/$name.txt"; else scrub <"$BINDIR/$name.run" >>"$OUT/$name.txt"; fi
      [ $rc -eq 0 ] || rc_all=$rc
    done <<EOR
$runs
EOR
    sanrep=0; grep -q -E "runtime error:|ERROR: (Address|Thread)Sanitizer|WARNING: ThreadSanitizer" "$OUT/$name.txt" && sanrep=1
    if [ "$expect" = run-fail ]; then { [ $rc_all -ne 0 ] || [ $sanrep = 1 ]; } || { ok=0; why="expected run failure, got exit 0"; }
    else { [ $rc_all -eq 0 ] && [ $sanrep = 0 ]; } || { ok=0; why="run exit code $rc_all or sanitizer report"; }; fi
  fi
  if [ $ok = 1 ] && [ "$san" = none ] && [ "$expect" = ok ]; then
    (cd "$HERE" && $CXX -std=$std -O2 -Wall -Wextra -fsanitize=address,undefined $extra "$f" -o "$bin.san") >/dev/null 2>&1 \
      && (cd "$HERE/$(basename "$(dirname "$f")")" && export QUICK=1 && while IFS= read -r c; do BIN="$bin.san" run_cmd "$c" || exit 1; done <<<"$runs") >/dev/null 2>&1 \
      || { ok=0; why="sanitizer build/run of timing file failed"; }
  fi
  if [ $ok = 1 ] && [ "$(directive "$f" ALSO none)" = thread ]; then
    (cd "$HERE" && $CXX -std=$std -O1 -Wall -Wextra -fsanitize=thread $extra "$f" -o "$bin.tsan") >/dev/null 2>&1 \
      && (cd "$HERE/$(basename "$(dirname "$f")")" && run_cmd "$bin.tsan") >"$BINDIR/$name.tsan.run" 2>&1 \
      && ! grep -q "WARNING: ThreadSanitizer" "$BINDIR/$name.tsan.run" \
      && { echo "(also run under ThreadSanitizer: no reports)" >>"$OUT/$name.txt"; } \
      || { ok=0; why="ThreadSanitizer build/run reported problems"; }
  fi
  if [ "$(directive "$f" ASM no)" = yes ]; then
    (cd "$HERE" && $CXX -std=$std -O2 -S "$f" -o "$OUT/$name.s") >/dev/null 2>&1 || { ok=0; why="asm failed"; }
  fi
  if [ $ok = 1 ]; then pass=$((pass+1)); echo "PASS  $(basename "$(dirname "$f")")/$name ($expect)"
  else fail=$((fail+1)); failed="$failed $name"; echo "FAIL  $(basename "$(dirname "$f")")/$name: $why"; fi
done
echo "---- $pass passed, $fail failed${failed:+:$failed}"
[ $fail -eq 0 ]
