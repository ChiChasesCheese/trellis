import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.StandardSocketOptions;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Arrays;

/**
 * ld03 讲义配套实验（本机回环；测的是软件 + 内核开销，不是网线）。
 *
 * 编译 / 运行（在 kit 根目录）：
 *   javac --release 21 --enable-preview -d /tmp/ld03bench loop/rounds/03_lld/ld03_async_tcp_channel/reference/*.java study/30-articles/examples/ld03/ChannelBench.java
 *   java --enable-preview -cp /tmp/ld03bench ChannelBench
 *
 * 1. 吞吐：32 字节消息，发送线程 offer / 接收线程 poll，各跑 3 次取中位数
 * 2. 往返：一问一答 32 字节，100,000 次，报 p50 / p99 / p99.9 / max（对照：裸的阻塞 SocketChannel 乒乓）
 * 3. 背压：接收端不读时，发送端在 offer 返回 false 之前接受了多少条（小缓冲区）
 */
public class ChannelBench {
    public static void main(String[] args) throws Exception {
        System.out.println("java " + System.getProperty("java.version") + ", " + Runtime.getRuntime().availableProcessors() + " cores, " + System.getProperty("os.name"));
        throughput();
        roundTrip();
        backpressure();
    }

    // ------------------------------------------------------------------ 1
    static void throughput() throws Exception {
        ChannelConfig cfg = new ChannelConfig(1024, 64 * 1024, 64 * 1024);
        int n = 2_000_000;
        long[] ms = new long[3];
        for (int run = 0; run < 3; run++) {
            try (MessageServer srv = new MessageServer(0, cfg);
                 TcpMessageChannel c = TcpMessageChannel.connect(srv.address(), cfg)) {
                TcpMessageChannel s = srv.accept(5_000);
                byte[] payload = new byte[32];
                Thread sender = new Thread(() -> {
                    try { for (int i = 0; i < n; i++) c.offer(payload, 10_000); } catch (Exception e) { throw new RuntimeException(e); }
                });
                long t0 = System.nanoTime();
                sender.start();
                for (int i = 0; i < n; i++) if (s.poll(10_000) == null) throw new IllegalStateException("lost at " + i);
                ms[run] = (System.nanoTime() - t0) / 1_000_000;
                sender.join();
                s.close();
            }
        }
        Arrays.sort(ms);
        System.out.printf("throughput: %,d msgs x 32 B in %d ms (median of 3: runs=%s) => %.2f M msg/s%n", n, ms[1], Arrays.toString(ms), n / (ms[1] / 1000.0) / 1e6);
    }

    // ------------------------------------------------------------------ 2
    static void roundTrip() throws Exception {
        ChannelConfig cfg = new ChannelConfig(1024, 16 * 1024, 16 * 1024);
        int warm = 20_000, n = 100_000;
        long[] ours = new long[n];
        try (MessageServer srv = new MessageServer(0, cfg);
             TcpMessageChannel c = TcpMessageChannel.connect(srv.address(), cfg)) {
            TcpMessageChannel s = srv.accept(5_000);
            Thread echo = new Thread(() -> {
                try {
                    for (int i = 0; i < warm + n; i++) { byte[] m = s.poll(10_000); s.offer(m, 10_000); }
                } catch (Exception e) { throw new RuntimeException(e); }
            });
            echo.start();
            byte[] payload = new byte[32];
            for (int i = 0; i < warm + n; i++) {
                long t0 = System.nanoTime();
                c.offer(payload, 10_000);
                c.poll(10_000);
                if (i >= warm) ours[i - warm] = System.nanoTime() - t0;
            }
            echo.join();
        }
        report("our channel  ", ours);

        // 对照：裸阻塞 SocketChannel 乒乓（同样 4 字节头 + 32 字节负载，同样 TCP_NODELAY）
        long[] raw = new long[n];
        try (ServerSocketChannel ss = ServerSocketChannel.open().bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0));
             SocketChannel cl = SocketChannel.open(ss.getLocalAddress())) {
            cl.setOption(StandardSocketOptions.TCP_NODELAY, true);
            SocketChannel sv = ss.accept();
            sv.setOption(StandardSocketOptions.TCP_NODELAY, true);
            Thread echo = new Thread(() -> {
                try {
                    ByteBuffer b = ByteBuffer.allocate(36);
                    for (int i = 0; i < warm + n; i++) {
                        b.clear();
                        while (b.hasRemaining()) if (sv.read(b) < 0) return;
                        b.flip();
                        while (b.hasRemaining()) sv.write(b);
                    }
                } catch (Exception e) { throw new RuntimeException(e); }
            });
            echo.start();
            ByteBuffer out = ByteBuffer.allocate(36), in = ByteBuffer.allocate(36);
            for (int i = 0; i < warm + n; i++) {
                out.clear(); out.putInt(32).put(new byte[32]).flip();
                long t0 = System.nanoTime();
                while (out.hasRemaining()) cl.write(out);
                in.clear();
                while (in.hasRemaining()) if (cl.read(in) < 0) throw new IllegalStateException();
                if (i >= warm) raw[i - warm] = System.nanoTime() - t0;
            }
            echo.join();
            sv.close();
        }
        report("raw blocking ", raw);
    }

    static void report(String name, long[] ns) {
        long[] a = ns.clone();
        Arrays.sort(a);
        System.out.printf("round-trip %s: p50 %.1f us, p99 %.1f us, p99.9 %.1f us, max %.1f us%n", name,
                a[a.length / 2] / 1e3, a[(int) (a.length * 0.99)] / 1e3, a[(int) (a.length * 0.999)] / 1e3, a[a.length - 1] / 1e3);
    }

    // ------------------------------------------------------------------ 3
    static void backpressure() throws Exception {
        for (int[] caps : new int[][]{{4 * 1024, 4 * 1024}, {64 * 1024, 64 * 1024}}) {
            ChannelConfig cfg = new ChannelConfig(256, caps[0], caps[1]);
            ServerSocketChannel ss = ServerSocketChannel.open();
            ss.setOption(StandardSocketOptions.SO_RCVBUF, 4096);
            ss.bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0));
            SocketChannel c = SocketChannel.open();
            c.setOption(StandardSocketOptions.SO_SNDBUF, 4096);
            c.connect(ss.getLocalAddress());
            SocketChannel s = ss.accept();
            ss.close();
            s.setOption(StandardSocketOptions.SO_RCVBUF, 4096);
            try (TcpMessageChannel cc = TcpMessageChannel.wrap(c, cfg); TcpMessageChannel sc = TcpMessageChannel.wrap(s, cfg)) {
                byte[] payload = new byte[32];
                long accepted = 0;
                while (accepted < 5_000_000 && cc.offer(payload, 200)) accepted++;
                System.out.printf("backpressure: rings %d/%d B, SO_SNDBUF/RCVBUF requested 4096 -> sender accepted %,d msgs (%,d framed bytes) before a 200 ms stall%n",
                        caps[0], caps[1], accepted, accepted * 36);
                long got = 0;
                while (sc.poll(500) != null) got++;
                System.out.printf("   receiver then drained %,d msgs (equal: %b)%n", got, got == accepted);
            }
        }
    }
}
