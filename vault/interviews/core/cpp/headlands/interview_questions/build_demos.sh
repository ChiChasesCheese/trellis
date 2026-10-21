#!/usr/bin/env bash
# Build and run every demo in demos/.
#   ./build_demos.sh          sanitizer build of every demo (must run clean), then the -O2 runs, asm checks,
#                             the compile-error files and the "expected to fail" files, with their output
#   ./build_demos.sh quick    only the sanitizer pass/fail table
# Flags: clang++ -std=c++20 -O2 -Wall -Wextra -fsanitize=address,undefined   (C++23 demo: -std=c++23)
# Needs clang++ with libc++ (Apple clang on macOS). Takes about a minute.
set -u
exec </dev/null                                         # the ASan symbolizer can block on an inherited stdin
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/demos" || exit 1
CXX=${CXX:-clang++}
OUT="${TMPDIR:-/tmp}/kq_cpp_demos"
mkdir -p "$OUT"
STD="-std=c++20"
WARN="-Wall -Wextra"
SAN="-fsanitize=address,undefined"

# demos that need special handling in the sanitizer pass
SKIP='q03_|q07_|q25_err_|_bad$|_warn$|_error$|_hardening$|q42_loop'     # multi-file, per-standard, expected-to-fail, python
EXTRA_STD_q10_cpp23="-std=c++23"
# NOSYM=1 turns off sanitizer symbolization (the macOS symbolizer, atos, can block on machines without Developer Mode)
SYM=${NOSYM:+:symbolize=0}
export ASAN_OPTIONS="allocator_may_return_null=1$SYM"   # q12 asks malloc for an impossible size on purpose
export TSAN_OPTIONS="${SYM#:}"
export UBSAN_OPTIONS="${SYM#:}"

limit() { perl -e 'alarm 120; exec @ARGV' "$@"; }          # no `timeout` on macOS: kill anything that hangs
pass=0; fail=0
echo "== sanitizer pass (address,undefined): every demo must exit 0 =="
for f in q*.cpp; do
  n=${f%.cpp}
  if [[ $n =~ $SKIP ]]; then continue; fi
  std=$STD; [[ $n == q10_cpp23 ]] && std="-std=c++23"
  if $CXX $std -O2 $WARN $SAN "$f" -o "$OUT/$n.san" 2>"$OUT/$n.log" && limit "$OUT/$n.san" >"$OUT/$n.out" 2>>"$OUT/$n.log"; then
    pass=$((pass+1)); printf '  ok    %s\n' "$n"
  else
    fail=$((fail+1)); printf '  FAIL  %s (see %s)\n' "$n" "$OUT/$n.log"
  fi
done
echo "sanitizer pass: $pass ok, $fail failed"
[[ ${1:-} == quick ]] && exit $((fail > 0))

cap() { limit "$@" >"$OUT/cap.txt" 2>&1; }              # never pipe a sanitizer report straight into head (it can block)
show() { printf '\n$ %s\n' "${@: -1}" | sed "s#$OUT/##"; "$@" 2>&1; }
plain() {   # plain -O2 build and run (timings are only meaningful without sanitizers)
  local n=$1; shift
  $CXX ${STD_OVERRIDE:-$STD} -O2 $WARN "$@" "$n.cpp" -o "$OUT/$n" && show limit "$OUT/$n"
}
section() { printf '\n\n######## %s\n' "$*"; }

section "Q01 / Q04: std::sort vs qsort, -O0 vs -O2"
plain q01_sort_vs_qsort

section "Q02: contiguous vs boxed"
plain q02_contiguous

section "Q03: translation units, linking, ODR"
$CXX $STD -c q03_lib.cpp -o "$OUT/q03_lib.o" && $CXX $STD -c q03_main.cpp -o "$OUT/q03_main.o"
echo '$ nm q03_lib.o q03_main.o   (T = defined here, U = needed from elsewhere)'; nm "$OUT/q03_lib.o" "$OUT/q03_main.o" | grep -E ' [TU] '
$CXX "$OUT/q03_lib.o" "$OUT/q03_main.o" -o "$OUT/q03" && show "$OUT/q03"
echo '$ clang++ q03_undefined.cpp'; $CXX $STD q03_undefined.cpp -o "$OUT/u" 2>&1 | head -6
echo '$ clang++ q03_dup.cpp q03_dup_main.cpp'; $CXX $STD q03_dup.cpp q03_dup_main.cpp -o "$OUT/d" 2>&1 | head -2
printf '#include <iostream>\nint main(){}\n' > "$OUT/inc_iostream.cpp"; printf '#include <cstdio>\nint main(){}\n' > "$OUT/inc_cstdio.cpp"
echo "lines after preprocessing <iostream>: $($CXX $STD -E "$OUT/inc_iostream.cpp" | wc -l)"
echo "lines after preprocessing <cstdio>  : $($CXX $STD -E "$OUT/inc_cstdio.cpp" | wc -l)"

section "Q04: generated code (-S)"
$CXX $STD -O2 -S q04_zero_overhead.cpp -o "$OUT/q04_O2.s"
$CXX $STD -O0 -S q04_zero_overhead.cpp -o "$OUT/q04_O0.s"
body() { awk -v f="$2" '$0 ~ "^__Z[0-9]*"f"[A-Za-z0-9_]*:" {p=1} p {print} /\.cfi_endproc/ {if(p) exit}' "$1"; }
for fn in sum_loop sum_acc sum_lambda; do
  printf '%-11s -O0: %3d instructions, %d calls | -O2: %3d instructions, %d calls, %2d SIMD ops\n' "$fn" \
    "$(body "$OUT/q04_O0.s" $fn | grep -cE '^\s+[a-z]')" "$(body "$OUT/q04_O0.s" $fn | grep -cE '^\s+bl\s')" \
    "$(body "$OUT/q04_O2.s" $fn | grep -cE '^\s+[a-z]')" "$(body "$OUT/q04_O2.s" $fn | grep -cE '^\s+bl\s')" \
    "$(body "$OUT/q04_O2.s" $fn | grep -cE '\.(2d|4s)')"
done
echo "gauss(n) at -O2 (a loop became arithmetic):"; body "$OUT/q04_O2.s" gauss | grep -E '^\s+[a-z]' | grep -v cfi
plain q04_zero_overhead

section "Q05: virtual"
plain q05_virtual
plain q05_virtual_dtor

section "Q06: locality"
plain q06_locality

section "Q07: the same file under each -std"
for s in c++11 c++14 c++17 c++20 c++23; do
  $CXX -std=$s q07_standard.cpp -o "$OUT/q07_$s" && { echo "-std=$s"; "$OUT/q07_$s" | sed 's/^/    /'; }
done
printf 'int main(){ auto f = [](auto x){ return x; }; return f(0); }\n' > "$OUT/generic_lambda.cpp"
echo '$ clang++ -std=c++11 generic lambda:'; $CXX -std=c++11 -c "$OUT/generic_lambda.cpp" -o /dev/null 2>&1 | head -2
STD_OVERRIDE=-std=c++11 plain q08_cpp11
STD_OVERRIDE=-std=c++17 plain q09_cpp14_17
plain q10_cpp20
STD_OVERRIDE=-std=c++23 plain q10_cpp23

section "Q11 - Q16"
plain q11_raii
plain q12_malloc_new
plain q13_smart_ptrs
plain q14_move
echo '$ clang++ -Wall q14_move_warn.cpp'; $CXX $STD $WARN -c q14_move_warn.cpp -o /dev/null 2>&1 | head -3
plain q15_copy_vs_memcpy
$CXX $STD -O2 -S q15_copy_vs_memcpy.cpp -o "$OUT/q15.s"
echo "std::copy of int[] compiles to: $(body "$OUT/q15.s" copy_ints | grep -E '^\s+bl\s' | tr -s ' \t' ' ')"
plain q16_layout
echo '$ ASAN_OPTIONS=alloc_dealloc_mismatch=1 (new[] / delete)'
$CXX $STD -w -g $SAN q12_mismatch_bad.cpp -o "$OUT/q12_bad" && cap env ASAN_OPTIONS="alloc_dealloc_mismatch=1$SYM" "$OUT/q12_bad"; head -3 "$OUT/cap.txt"

section "Q17 - Q19: containers"
plain q17_vector
echo '$ ASan on q17_invalid_iterator_bad.cpp'; $CXX $STD -g $SAN q17_invalid_iterator_bad.cpp -o "$OUT/q17_bad" && { cap "$OUT/q17_bad"; head -4 "$OUT/cap.txt"; }
plain q18_maps
plain q19_erase

section "Q20 - Q22: templates"
plain q20_templates
echo '$ clang++ q20_concept_error.cpp'; $CXX $STD q20_concept_error.cpp -o /dev/null 2>&1 | grep -E 'error|note: (candidate|because)'
echo '$ clang++ q20_no_concept_error.cpp'; $CXX $STD q20_no_concept_error.cpp -o /dev/null 2>&1 | grep -E 'error|note'
plain q21_forwarding
plain q22_constexpr

section "Q23: undefined behaviour"
$CXX $STD -O0 q23_ub_overflow.cpp -o "$OUT/ub0" && echo "-O0:" && "$OUT/ub0"
echo "-O2:"; plain q23_ub_overflow
echo '-O2 -fsanitize=undefined:'; $CXX $STD -O2 -fsanitize=undefined q23_ub_overflow.cpp -o "$OUT/ub_san" && { cap "$OUT/ub_san"; head -4 "$OUT/cap.txt"; }
echo '$ UBSan tour'; $CXX $STD -O2 -fsanitize=undefined q23_ubsan_tour.cpp -o "$OUT/tour" && { cap "$OUT/tour"; grep -v SUMMARY "$OUT/cap.txt"; }

section "Q24: sanitizers (each is expected to report)"
for n in q24_asan_overflow_bad q24_asan_uaf_bad q24_stack_bad; do
  echo "--- $n"; $CXX $STD -g $SAN "$n.cpp" -o "$OUT/$n" && { cap "$OUT/$n"; grep -E 'ERROR|SUMMARY|READ|WRITE|located|^\s+#[0-3] .* in main|name' "$OUT/cap.txt" | head -7; }
done
echo "--- q24_tsan_race_bad (ThreadSanitizer)"; $CXX $STD -g -fsanitize=thread q24_tsan_race_bad.cpp -o "$OUT/tsan" && { cap "$OUT/tsan"; grep -E 'WARNING|Write of|Previous write|SUMMARY|^\s+#4 main' "$OUT/cap.txt" | head -5; }
echo "--- clean programs under TSan"
for n in q28_mutex_cv q29_atomics; do $CXX $STD -O1 -g -fsanitize=thread "$n.cpp" -o "$OUT/$n.tsan" && { cap "$OUT/$n.tsan"; echo "$n: TSan warnings = $(grep -c 'WARNING: ThreadSanitizer' "$OUT/cap.txt")"; }; done

section "Q25: compile errors (first lines of each), then the fixed file"
plain q25_fixed
for n in missing_include const narrowing no_match typename semicolon return; do
  echo "--- q25_err_$n.cpp"; $CXX $STD $WARN -c "q25_err_$n.cpp" -o /dev/null 2>&1 | grep -E 'error|warning' | grep -v '^In file' | head -4
done

section "Q26: bits"
plain q26_bits

section "Q27: debugging"
$CXX $STD -g -O0 q27_debug_target.cpp -o "$OUT/dbg" && show "$OUT/dbg"
echo '$ -D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG q27_hardening.cpp'
$CXX $STD -g -O0 -D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG q27_hardening.cpp -o "$OUT/hard" && { cap "$OUT/hard"; head -2 "$OUT/cap.txt"; }

section "Q28 - Q31: concurrency"
plain q28_mutex_cv
plain q29_atomics
$CXX $STD -O2 -S q29_atomics.cpp -o "$OUT/q29.s"
echo "fetch_add code on this CPU:  seq_cst -> $(body "$OUT/q29.s" bump_seq_cst | grep -oE '(ldadd|ldaddal|lock xadd)[a-z]*' | head -1) | relaxed -> $(body "$OUT/q29.s" bump_relaxed | grep -oE '(ldadd|ldaddal|lock xadd)[a-z]*' | head -1)"
plain q30_volatile_race
plain q31_false_sharing

section "Q32 - Q35: OS and IPC"
plain q32_vm_fork
plain q33_ipc_pipes
plain q34_shm_ring
plain q35_pingpong

section "Q36 - Q39: low-latency idioms"
plain q36_pmr_arena
plain q37_spsc_queue
plain q38_branches
plain q39_errors

section "Q40 - Q44: Java / Python / live coding"
plain q40_java_idioms
plain q41_value_semantics
echo '$ ASan with detect_stack_use_after_return=1 on q41_dangling_bad.cpp'
$CXX $STD -w -g -fsanitize=address q41_dangling_bad.cpp -o "$OUT/dang" && { cap env ASAN_OPTIONS="detect_stack_use_after_return=1$SYM" "$OUT/dang"; head -2 "$OUT/cap.txt"; }
plain q42_python_vs_cpp
if command -v python3 >/dev/null; then python3 q42_loop.py; fi
plain q44_live_skeleton

exit $((fail > 0))
