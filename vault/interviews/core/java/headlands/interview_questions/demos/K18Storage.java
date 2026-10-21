import java.io.*;
import java.nio.*;
import java.nio.channels.FileChannel;
import java.nio.file.*;

/** Page cache, write(), fsync (FileChannel.force), mmap -- what "durable" costs. */
public class K18Storage {
    public static void main(String[] a) throws Exception {
        Path dir = Files.createTempDirectory("k18");
        int recs = 2000; ByteBuffer rec = ByteBuffer.allocateDirect(4096);
        for (var mode : new String[]{"write only (page cache)", "write + force() after EVERY record", "write all, one force() at end", "mmap store + force() at end"}) {
            Path f = dir.resolve("f" + mode.hashCode());
            long t0 = System.nanoTime();
            try (FileChannel ch = FileChannel.open(f, StandardOpenOption.CREATE, StandardOpenOption.WRITE, StandardOpenOption.READ)) {
                if (mode.startsWith("mmap")) {
                    MappedByteBuffer mb = ch.map(FileChannel.MapMode.READ_WRITE, 0, (long) recs * 4096);
                    for (int i = 0; i < recs; i++) { mb.putInt(i * 4096, i); }
                    mb.force();
                } else for (int i = 0; i < recs; i++) {
                    rec.clear(); rec.putInt(i); rec.position(0).limit(4096); ch.write(rec);
                    if (mode.contains("EVERY")) ch.force(false);
                }
                if (mode.contains("one force")) ch.force(false);
            }
            long ms = (System.nanoTime() - t0) / 1_000_000;
            System.out.printf("%-38s %2d recs x 4KB: %6d ms%n", mode, recs, ms);
        }
        long t0 = System.nanoTime(); long sum = 0;
        for (Path p : Files.newDirectoryStream(dir)) sum += Files.readAllBytes(p).length;
        System.out.printf("re-read %d MB just written: %d ms (served from page cache)%n", sum >> 20, (System.nanoTime() - t0) / 1_000_000);
        try (var ds = Files.newDirectoryStream(dir)) { for (Path p : ds) Files.delete(p); } Files.delete(dir);
        System.out.println("os.name=" + System.getProperty("os.name"));
    }
}
