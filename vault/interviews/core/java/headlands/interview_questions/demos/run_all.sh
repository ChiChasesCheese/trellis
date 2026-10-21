#!/usr/bin/env bash
# Compile and run every demo; write transcripts to OUTPUTS.txt.  Usage: ./run_all.sh   (about 3 minutes)
set -u
B=/opt/homebrew/opt/openjdk@21/bin
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT=/tmp/kqout; rm -rf "$OUT"; mkdir -p "$OUT"
$B/javac --release 21 --enable-preview -d "$OUT" "$HERE"/K*.java 2>&1 | grep -v '^Note' 
T="$HERE/OUTPUTS.txt"
{
echo "# $(date '+%Y-%m-%d') | $($B/java -version 2>&1 | head -1) | $(uname -sm) | cores=$(sysctl -n hw.ncpu 2>/dev/null)"
r() { echo; echo "\$ $*"; "$@" 2>&1; }
cd "$OUT"
r $B/java --enable-preview K01Visibility
r $B/java -Xint --enable-preview K01Visibility
r $B/java --enable-preview K02Boxing
r $B/java --enable-preview K03ObjectSize
r $B/java --enable-preview K04EscapeAnalysis
r $B/java --enable-preview -XX:-DoEscapeAnalysis K04EscapeAnalysis
r $B/java --enable-preview K05Strings
r $B/javap -c -p K05Concat
r $B/java --add-opens java.base/java.util=ALL-UNNAMED K06HashMap
r $B/java K07Chm
r $B/java K08Counters
r $B/java K22VolatileCounter
r $B/java --enable-preview K09VirtualThreads
r $B/java -Djdk.virtualThreadScheduler.parallelism=1 -Djdk.virtualThreadScheduler.maxPoolSize=1 K09Pinning
r $B/java K10Jit
echo; echo '$ java -XX:+PrintCompilation K10Jit | grep -E "K10Jit::run|Tri::area|Cir::area"'; $B/java -XX:+PrintCompilation K10Jit 2>&1 | grep -E "K10Jit::run|Tri::area|Cir::area"
echo; echo '$ java -XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining K10Jit | grep area (unique lines)'; $B/java -XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining K10Jit 2>&1 | grep -E "area" | sed 's/^ *//' | sort | uniq -c
r $B/java --enable-preview -XX:MaxDirectMemorySize=16m K11OffHeap
r $B/java K12ArrayCopy
r $B/java K13SmartPtr
r $B/java --enable-preview K14Versions
r $B/java K15Overflow
r $B/java K16Ipc
r $B/java K17Nagle
r $B/java K18Storage
r $B/java -Xmx3g K21Locality
r $B/java -XX:+UseBiasedLocking -version
echo; echo '$ java -Xlog:safepoint -Xms512m -Xmx512m -XX:+UseG1GC K19Pauses | grep safepoint | head -3'; $B/java -Xlog:safepoint -Xms512m -Xmx512m -XX:+UseG1GC K19Pauses 2>&1 | grep -i safepoint | head -3
for gc in "-XX:+UseParallelGC" "-XX:+UseG1GC" "-XX:+UseZGC -XX:+ZGenerational"; do r $B/java -Xms1g -Xmx1g $gc K19Pauses; done
r $B/java -Xms1g -Xmx1g -XX:+UseG1GC K19Pauses nochurn
echo; echo '$ jcmd/jstat against K20Busy'
$B/java -Xmx256m -XX:+UseG1GC K20Busy 12000 & PID=$!; sleep 3
$B/jstat -gcutil $PID 500 3
$B/jcmd $PID GC.heap_info
$B/jcmd $PID Thread.print | grep -A5 -E '"(waits-for-lock|holds-lock)"'
$B/jcmd $PID GC.class_histogram | head -5
kill $PID 2>/dev/null; wait $PID 2>/dev/null
echo; echo "# --- JDK tools (run_tools.sh) ---"; echo; "$HERE/run_tools.sh"
} > "$T" 2>&1
echo "wrote $T"
