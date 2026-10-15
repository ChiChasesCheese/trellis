import java.io.*;
import java.lang.invoke.*;
import java.net.*;
import java.nio.*;
import java.nio.channels.FileChannel;
import java.nio.file.*;

/**
 * Round-trip latency of three IPC mechanisms between two JVM processes (same machine):
 *   pipe (child's stdin/stdout), loopback TCP socket, shared mapped file with spin on a volatile sequence.
 * Run:  java K16Ipc          (parent spawns itself as "child <mode> ...")
 */
public class K16Ipc {
    static final int N = 50_000;
    static final VarHandle LONGS = MethodHandles.byteBufferViewVarHandle(long[].class, ByteOrder.nativeOrder());

    public static void main(String[] a) throws Exception {
        if (a.length > 0) { child(a); return; }
        pipe(); socket(); mmap();
    }
    static Process spawn(String... args) throws IOException {
        String javaBin = Path.of(System.getProperty("java.home"), "bin", "java").toString();
        var cmd = new java.util.ArrayList<>(java.util.List.of(javaBin, "-cp", System.getProperty("java.class.path"), "K16Ipc"));
        cmd.addAll(java.util.List.of(args));
        return new ProcessBuilder(cmd).redirectError(ProcessBuilder.Redirect.INHERIT).start();
    }
    static void report(String name, long ns) { System.out.printf("%-34s %8.2f us per round trip%n", name, ns / 1000.0 / N); }

    static void pipe() throws Exception {
        Process p = spawn("pipe");
        OutputStream out = p.getOutputStream(); InputStream in = p.getInputStream();
        for (int i = 0; i < 2000; i++) { out.write(1); out.flush(); in.read(); }
        long t0 = System.nanoTime();
        for (int i = 0; i < N; i++) { out.write(1); out.flush(); in.read(); }
        report("pipe (stdin/stdout)", System.nanoTime() - t0); out.close(); p.waitFor();
    }
    static void socket() throws Exception {
        try (ServerSocket ss = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Process p = spawn("socket", String.valueOf(ss.getLocalPort()));
            try (Socket s = ss.accept()) {
                s.setTcpNoDelay(true); var in = s.getInputStream(); var out = s.getOutputStream();
                for (int i = 0; i < 2000; i++) { out.write(1); out.flush(); in.read(); }
                long t0 = System.nanoTime();
                for (int i = 0; i < N; i++) { out.write(1); out.flush(); in.read(); }
                report("loopback TCP (NODELAY)", System.nanoTime() - t0);
            }
            p.waitFor();
        }
    }
    static void mmap() throws Exception {
        Path f = Files.createTempFile("k16", ".shm");
        try (FileChannel ch = FileChannel.open(f, StandardOpenOption.READ, StandardOpenOption.WRITE)) {
            MappedByteBuffer mb = ch.map(FileChannel.MapMode.READ_WRITE, 0, 4096);
            LONGS.setVolatile(mb, 0, 0L); LONGS.setVolatile(mb, 64, 0L);
            Process p = spawn("mmap", f.toString());
            int warm = 2000;
            for (long i = 1; i <= warm; i++) { LONGS.setVolatile(mb, 0, i); while ((long) LONGS.getVolatile(mb, 64) != i) Thread.onSpinWait(); }
            long t0 = System.nanoTime();
            for (long i = warm + 1; i <= warm + N; i++) { LONGS.setVolatile(mb, 0, i); while ((long) LONGS.getVolatile(mb, 64) != i) Thread.onSpinWait(); }
            report("shared mmap, spin on volatile seq", System.nanoTime() - t0);
            LONGS.setVolatile(mb, 0, -1L); p.waitFor();
        } finally { Files.deleteIfExists(f); }
    }
    static void child(String[] a) throws Exception {
        switch (a[0]) {
            case "pipe" -> { int b; var in = new BufferedInputStream(System.in, 1); var out = System.out; while ((b = System.in.read()) != -1) { out.write(b); out.flush(); } }
            case "socket" -> { try (Socket s = new Socket(InetAddress.getLoopbackAddress(), Integer.parseInt(a[1]))) {
                s.setTcpNoDelay(true); var in = s.getInputStream(); var out = s.getOutputStream(); int b;
                while ((b = in.read()) != -1) { out.write(b); out.flush(); } } }
            case "mmap" -> { try (FileChannel ch = FileChannel.open(Path.of(a[1]), StandardOpenOption.READ, StandardOpenOption.WRITE)) {
                MappedByteBuffer mb = ch.map(FileChannel.MapMode.READ_WRITE, 0, 4096); long last = 0;
                while (true) { long v = (long) LONGS.getVolatile(mb, 0); if (v == -1) break; if (v != last) { last = v; LONGS.setVolatile(mb, 64, v); } else Thread.onSpinWait(); } } }
        }
    }
}
