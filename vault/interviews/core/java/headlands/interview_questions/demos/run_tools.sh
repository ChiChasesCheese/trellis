#!/usr/bin/env bash
# JDK diagnostic tools against the busy JVM (K20Busy): Native Memory Tracking, RSS, JFR hot methods.
# Needs /tmp/kqout (created by run_all.sh).  Output is appended to OUTPUTS.txt by hand (see end of that file).
B=/opt/homebrew/opt/openjdk@21/bin
cd /tmp/kqout || exit 1
$B/java -Xmx256m -XX:NativeMemoryTracking=summary -XX:StartFlightRecording=duration=6s,filename=/tmp/k20.jfr,settings=profile K20Busy 9000 > /dev/null 2>&1 &
PID=$!; sleep 4
echo '$ jcmd PID VM.native_memory summary   (java -Xmx256m -XX:NativeMemoryTracking=summary)'
$B/jcmd $PID VM.native_memory summary | grep -E "^Total|^-  *(Java Heap|Class |Thread|Code|GC |Metaspace|Shared class|Arena)" | cut -c1-120
echo '$ ps -o rss= -p PID    (KB)'; ps -o rss= -p $PID
wait $PID
echo '$ jfr view hot-methods /tmp/k20.jfr'; $B/jfr view hot-methods /tmp/k20.jfr 2>&1 | head -10
