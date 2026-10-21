import jdk.jfr.Recording;
import jdk.jfr.consumer.RecordedEvent;
import jdk.jfr.consumer.RecordingFile;

import java.lang.management.ManagementFactory;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.*;

/**
 * J19 例 5：JFR（Java Flight Recorder）——JVM 内置的、开销很低的事件记录器。这里用代码启动一次录制，
 * 只开 GC 暂停事件(jdk.GCPhasePause)，跑一段分配密集的负载，然后读回事件统计"暂停多久"。
 * 命令行等价物：java -XX:StartFlightRecording:filename=rec.jfr,settings=profile ...；然后 `jfr print --events jdk.GCPhasePause rec.jfr`
 */
public class J19Ex5Jfr {
    public static void main(String[] args) throws Exception {
        int liveCount = 4_000_000;
        List<byte[]> live = new ArrayList<>(liveCount);
        for (int i = 0; i < liveCount; i++) live.add(new byte[100]);

        Path file = Files.createTempFile("j19", ".jfr");
        try (Recording rec = new Recording()) {
            rec.enable("jdk.GCPhasePause").withThreshold(Duration.ZERO);
            rec.start();
            long end = System.nanoTime() + 8_000_000_000L;
            var rnd = new Random(1);
            long sink = 0;
            while (System.nanoTime() < end) {
                for (int i = 0; i < 1000; i++) {
                    byte[] g = new byte[200];
                    g[0] = 1; sink += g.length;
                    if ((i & 127) == 0) live.set(rnd.nextInt(liveCount), g);
                }
            }
            rec.stop();
            rec.dump(file);
            String gc = ManagementFactory.getGarbageCollectorMXBeans().stream().map(b -> b.getName()).toList().toString();
            List<Double> pausesMs = new ArrayList<>();
            for (RecordedEvent e : RecordingFile.readAllEvents(file)) pausesMs.add(e.getDuration().toNanos() / 1e6);
            Collections.sort(pausesMs);
            if (pausesMs.isEmpty()) { System.out.println(gc + ": 没有暂停事件"); return; }
            double sum = pausesMs.stream().mapToDouble(Double::doubleValue).sum();
            System.out.printf("%s%n  jdk.GCPhasePause 事件 %d 个, 总暂停 %.1f ms, 平均 %.3f ms, p99 %.3f ms, 最长 %.3f ms%n",
                    gc, pausesMs.size(), sum, sum / pausesMs.size(), pausesMs.get((int) (pausesMs.size() * 0.99)), pausesMs.get(pausesMs.size() - 1));
        } finally {
            Files.deleteIfExists(file);
        }
    }
}
