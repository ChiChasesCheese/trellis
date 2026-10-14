import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * Part 4：同一个环放进内存映射文件，两个独立的 JVM 进程各自 mmap 它。
 *
 * 子进程怎么启动：
 *   * java 可执行文件：ProcessHandle.current().info().command()（当前 JVM 自己的路径），取不到就退回 java.home/bin/java；
 *   * 类路径：System.getProperty("java.class.path") + 本测试类和被测类所在的目录/jar。
 *     后者是必须的：用 JUnit console 的 --class-path 跑时，java.class.path 只有 junit 的 jar，被测类在另一个类加载器里。
 *   * 必须带 --enable-preview：FFM API 在 JDK 21 是预览特性。
 * 每个测试至多启动一个子进程，整个类约 2–3 秒。
 */
class SharedChannelTest {
    private static final long CHILD_TIMEOUT_MS = 8_000;

    // ---------- 单进程内：两个映射共享同一个文件 ----------

    @Test @Tag("part4")
    void twoMappingsOfOneFileShareData(@TempDir Path dir) throws IOException {
        Path file = dir.resolve("chan.bin");
        try (var producer = SharedChannel.create(file, 1024); var consumer = SharedChannel.open(file)) {
            assertEquals(MessageRing.segmentBytes(1024), Files.size(file));
            assertEquals(1024, consumer.capacity());
            assertNull(consumer.receive());
            assertTrue(producer.send("hello".getBytes()));
            assertTrue(producer.send(new byte[0]));
            assertArrayEquals("hello".getBytes(), consumer.receive());
            assertArrayEquals(new byte[0], consumer.receive());
            assertNull(consumer.receive());
            assertFalse(consumer.isDrained());
            producer.finish();
            assertTrue(consumer.isDrained());
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void fullChannelRejectsAndRecovers(@TempDir Path dir) throws IOException {
        try (var a = SharedChannel.create(dir.resolve("c"), 64); var b = SharedChannel.open(dir.resolve("c"))) {
            int sent = 0;
            while (a.send(new byte[12])) sent++;
            assertEquals(4, sent);
            assertNotNull(b.receive());
            assertTrue(a.send(new byte[12]));
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void backlogSurvivesCloseAndReopen(@TempDir Path dir) throws IOException {
        Path file = dir.resolve("persist.bin");
        try (var p = SharedChannel.create(file, 4096)) {
            for (long i = 0; i < 20; i++) assertTrue(p.send(Msgs.make(i)));
        }                                               // 取消映射；数据在文件里
        try (var c = SharedChannel.open(file)) {
            for (long i = 0; i < 20; i++) assertNull(Msgs.check(c.receive(), i));
            assertNull(c.receive());
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void openRejectsFilesThatAreNotChannels(@TempDir Path dir) throws IOException {
        assertThrows(NoSuchFileException.class, () -> SharedChannel.open(dir.resolve("missing")));
        Path tiny = dir.resolve("tiny");
        Files.write(tiny, new byte[10]);
        assertThrows(IllegalStateException.class, () -> SharedChannel.open(tiny));
        Path zeros = dir.resolve("zeros");
        Files.write(zeros, new byte[4096]);
        assertThrows(IllegalStateException.class, () -> SharedChannel.open(zeros));
        Path noise = dir.resolve("noise");
        byte[] junk = new byte[4096];
        new java.util.Random(0).nextBytes(junk);
        Files.write(noise, junk);
        assertThrows(IllegalStateException.class, () -> SharedChannel.open(noise));
    }

    @Test @Tag("part4") @Tag("edge")
    void createRejectsBadCapacityAndCloseIsIdempotent(@TempDir Path dir) throws IOException {
        assertThrows(IllegalArgumentException.class, () -> SharedChannel.create(dir.resolve("x"), 100));
        var ch = SharedChannel.create(dir.resolve("y"), 64);
        ch.close();
        ch.close();
        assertThrows(IllegalStateException.class, () -> ch.send(new byte[1]));
        assertThrows(IllegalStateException.class, ch::receive);
        assertTrue(Files.exists(dir.resolve("y")), "close 只取消映射，不删文件");
    }

    // ---------- 跨进程 ----------

    @Test @Tag("part4") @Tag("io") @Tag("conc")
    void childProcessConsumesWhatTheParentProduces(@TempDir Path dir) throws Exception {
        Path file = dir.resolve("p2c.bin");
        final long n = 200_000;
        try (var ch = SharedChannel.create(file, 1 << 14)) {     // 16 KiB：远小于总数据量（约 6 MB），要回绕几百次
            Process child = spawn("consume", file, n);
            String err = SpscChild.produce(ch, n, System.nanoTime() + CHILD_TIMEOUT_MS * 1_000_000L);
            assertNull(err, "parent");
            assertChildOk(child, n);
        }
    }

    @Test @Tag("part4") @Tag("io") @Tag("conc")
    void parentConsumesWhatAChildProcessProduces(@TempDir Path dir) throws Exception {
        Path file = dir.resolve("c2p.bin");
        final long n = 200_000;
        try (var ch = SharedChannel.create(file, 1 << 12)) {     // 4 KiB：更小，回绕更频繁
            Process child = spawn("produce", file, n);
            String err = SpscChild.consume(ch, n, System.nanoTime() + CHILD_TIMEOUT_MS * 1_000_000L);
            assertNull(err, "parent");
            assertChildOk(child, n);
        }
    }

    @Test @Tag("part4") @Tag("io")
    void childReadsTheBacklogAParentLeftBehind(@TempDir Path dir) throws Exception {
        Path file = dir.resolve("backlog.bin");
        final long n = 50;
        try (var ch = SharedChannel.create(file, 1 << 12)) {
            assertNull(SpscChild.produce(ch, n, System.nanoTime() + 1_000_000_000L));
        }                                                       // 父进程已经取消映射、不再持有通道
        assertChildOk(spawn("consume", file, n), n);            // 子进程之后才启动，数据只能来自文件
    }

    // ---------- 工具 ----------

    private static Process spawn(String mode, Path file, long count) throws IOException {
        String java = ProcessHandle.current().info().command()
                .orElseGet(() -> Path.of(System.getProperty("java.home"), "bin", "java").toString());
        var cmd = new ArrayList<String>(List.of(java, "--enable-preview", "-XX:+UseSerialGC", "-Xshare:auto", "-cp", classPath(),
                "SpscChild", mode, file.toString(), Long.toString(count), Long.toString(CHILD_TIMEOUT_MS)));
        return new ProcessBuilder(cmd).redirectErrorStream(true).start();
    }

    /** 当前 JVM 的 java.class.path，加上 SpscChild 和 SharedChannel 所在的位置（去重，保持顺序）。 */
    private static String classPath() {
        var parts = new LinkedHashSet<String>();
        for (String p : System.getProperty("java.class.path", "").split(java.io.File.pathSeparator)) if (!p.isEmpty()) parts.add(p);
        for (Class<?> c : new Class<?>[] {SpscChild.class, SharedChannel.class, MessageRing.class}) {
            try {
                parts.add(Path.of(c.getProtectionDomain().getCodeSource().getLocation().toURI()).toString());
            } catch (Exception e) {
                throw new AssertionError("cannot locate " + c, e);
            }
        }
        return String.join(java.io.File.pathSeparator, parts);
    }

    private static void assertChildOk(Process child, long count) throws Exception {
        try {
            if (!child.waitFor(CHILD_TIMEOUT_MS + 2_000, TimeUnit.MILLISECONDS)) {
                fail("child did not finish in time");
            }
            String out = new String(child.getInputStream().readAllBytes()).strip();
            assertEquals(0, child.exitValue(), "child output: " + out);
            assertEquals("OK " + count, out);
        } finally {
            if (child.isAlive()) child.destroyForcibly();
        }
    }
}
