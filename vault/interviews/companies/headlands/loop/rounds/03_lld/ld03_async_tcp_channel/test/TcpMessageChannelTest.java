import static org.junit.jupiter.api.Assertions.*;

import java.io.EOFException;
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.StandardSocketOptions;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 2（通道：partial I/O、EOF、关闭）与 Part 3（背压、有界、压力）。全部走 127.0.0.1 临时端口。 */
class TcpMessageChannelTest {
    static final ChannelConfig CFG = new ChannelConfig(1024, 16 * 1024, 16 * 1024);

    private final List<AutoCloseable> toClose = new ArrayList<>();

    <T extends AutoCloseable> T track(T c) { toClose.add(c); return c; }

    @AfterEach
    void cleanup() throws Exception {
        for (AutoCloseable c : toClose) c.close();
    }

    record Pair(TcpMessageChannel client, TcpMessageChannel server) {}

    Pair pair(ChannelConfig cfg) throws Exception {
        MessageServer srv = track(new MessageServer(0, cfg));
        TcpMessageChannel client = track(TcpMessageChannel.connect(srv.address(), cfg));
        TcpMessageChannel server = track(srv.accept(5_000));
        assertNotNull(server, "server did not accept");
        return new Pair(client, server);
    }

    // ----------------------------------------------------------------------- Part 2

    @Test @Tag("part2") @Tag("io")
    void requestReply() throws Exception {
        var p = pair(CFG);
        assertNull(p.server().poll());
        assertTrue(p.client().offer("hello".getBytes()));
        assertArrayEquals("hello".getBytes(), p.server().poll(5_000));
        assertTrue(p.server().offer("world".getBytes()));
        assertArrayEquals("world".getBytes(), p.client().poll(5_000));
        assertTrue(p.client().isOpen());
        assertNull(p.client().failure());
    }

    @Test @Tag("part2") @Tag("io") @Tag("edge")
    void emptyAndMaxSizeMessages() throws Exception {
        var p = pair(CFG);
        byte[] max = new byte[CFG.maxFrame()];
        new java.util.Random(1).nextBytes(max);
        assertTrue(p.client().offer(new byte[0]));
        assertTrue(p.client().offer(max));
        assertTrue(p.client().offer(new byte[0]));
        assertArrayEquals(new byte[0], p.server().poll(5_000));
        assertArrayEquals(max, p.server().poll(5_000));
        assertArrayEquals(new byte[0], p.server().poll(5_000));
        assertThrows(IllegalArgumentException.class, () -> p.client().offer(new byte[CFG.maxFrame() + 1]));
        assertTrue(p.client().isOpen());                              // 非法参数不会弄坏通道
    }

    @Test @Tag("part2") @Tag("io")
    void pollTimeoutReturnsNullWhenNothingArrives() throws Exception {
        var p = pair(CFG);
        assertNull(p.server().poll(30));
        assertFalse(p.server().isDrained());
    }

    @Test @Tag("part2") @Tag("io") @Tag("conc")
    void tenThousandMessagesArriveInOrder() throws Exception {
        var p = pair(CFG);
        int n = 10_000;
        Thread sender = new Thread(() -> {
            try {
                for (int i = 0; i < n; i++) assertTrue(p.client().offer(Await.msg(i), 10_000), "offer timed out at " + i);
            } catch (Exception e) { throw new RuntimeException(e); }
        });
        sender.start();
        for (int i = 0; i < n; i++) {
            byte[] m = p.server().poll(10_000);
            assertTrue(Await.isMsg(m, i), "message " + i + " wrong or missing");
        }
        sender.join(5_000);
        assertNull(p.server().poll());
    }

    @Test @Tag("part2") @Tag("io") @Tag("perf")
    void twoHundredThousandMessagesThroughLoopbackFast() throws Exception {
        var p = pair(new ChannelConfig(1024, 64 * 1024, 64 * 1024));
        int n = 200_000;
        byte[] payload = new byte[32];
        assertTimeoutPreemptively(java.time.Duration.ofSeconds(5), () -> {
            Thread sender = new Thread(() -> {
                try { for (int i = 0; i < n; i++) assertTrue(p.client().offer(payload, 10_000)); } catch (Exception e) { throw new RuntimeException(e); }
            });
            sender.start();
            for (int i = 0; i < n; i++) assertNotNull(p.server().poll(10_000), "at " + i);
            sender.join();
        });
    }

    @Test @Tag("part2") @Tag("io") @Tag("conc")
    void bothDirectionsAtOnce() throws Exception {
        var p = pair(CFG);
        int n = 5_000;
        AtomicReference<Throwable> err = new AtomicReference<>();
        Runnable[] roles = new Runnable[2];
        TcpMessageChannel[] ends = {p.client(), p.server()};
        List<Thread> threads = new ArrayList<>();
        for (int side = 0; side < 2; side++) {
            TcpMessageChannel me = ends[side];
            int base = side * 1_000_000;
            int peerBase = (1 - side) * 1_000_000;
            threads.add(new Thread(() -> {
                try { for (int i = 0; i < n; i++) assertTrue(me.offer(Await.msg(base + i), 10_000)); } catch (Throwable t) { err.compareAndSet(null, t); }
            }));
            threads.add(new Thread(() -> {
                try { for (int i = 0; i < n; i++) assertTrue(Await.isMsg(me.poll(10_000), peerBase + i), "at " + i); } catch (Throwable t) { err.compareAndSet(null, t); }
            }));
        }
        threads.forEach(Thread::start);
        for (Thread t : threads) t.join(30_000);
        assertNull(err.get());
    }

    /** 用裸 socket 当对端，一个字节一个字节地发帧；通道不能在凑齐之前交出半条消息。 */
    @Test @Tag("part2") @Tag("io") @Tag("edge")
    void partialReadsAreReassembled() throws Exception {
        try (ServerSocketChannel ss = ServerSocketChannel.open().bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0));
             SocketChannel raw = SocketChannel.open(ss.getLocalAddress())) {
            raw.setOption(StandardSocketOptions.TCP_NODELAY, true);
            TcpMessageChannel ch = track(TcpMessageChannel.wrap(ss.accept(), CFG));
            byte[] payload = "split-me-into-pieces".getBytes();
            ByteBuffer frame = ByteBuffer.allocate(4 + payload.length).putInt(payload.length).put(payload).flip();
            for (int i = 0; i < 4 + 6; i++) raw.write(ByteBuffer.wrap(new byte[]{frame.get()}));      // 头 + 前 6 字节
            assertNull(ch.poll(100));                                                                    // 不完整：不能交出
            while (frame.hasRemaining()) raw.write(ByteBuffer.wrap(new byte[]{frame.get()}));
            assertArrayEquals(payload, ch.poll(5_000));
            // 一次写两条半
            ByteBuffer two = ByteBuffer.allocate(64).putInt(1).put((byte) 'a').putInt(2).put((byte) 'b').put((byte) 'c').putInt(3).put((byte) 'd').flip();
            raw.write(two);
            assertArrayEquals("a".getBytes(), ch.poll(5_000));
            assertArrayEquals("bc".getBytes(), ch.poll(5_000));
            assertNull(ch.poll(100));                                                                    // 第三条只有头 + 1 字节
            raw.write(ByteBuffer.wrap("ef".getBytes()));
            assertArrayEquals("def".getBytes(), ch.poll(5_000));
        }
    }

    @Test @Tag("part2") @Tag("io") @Tag("edge")
    void largeWriteIsSplitAcrossPartialWritesAndStaysIntact() throws Exception {
        // 一次性塞进几 MB：write 会返回部分写入，剩下的靠 OP_WRITE 继续
        ChannelConfig big = new ChannelConfig(1 << 20, 4 << 20, 2 << 20);
        var p = pair(big);
        byte[][] msgs = new byte[6][];
        java.util.Random rnd = new java.util.Random(9);
        for (int i = 0; i < msgs.length; i++) { msgs[i] = new byte[(1 << 19) + rnd.nextInt(1 << 19)]; rnd.nextBytes(msgs[i]); }
        for (byte[] m : msgs) assertTrue(p.client().offer(m, 10_000));
        for (byte[] m : msgs) assertArrayEquals(m, p.server().poll(10_000));
    }

    @Test @Tag("part2") @Tag("io") @Tag("edge")
    void invalidFrameHeaderFailsTheChannelButKeepsEarlierMessages() throws Exception {
        try (ServerSocketChannel ss = ServerSocketChannel.open().bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0));
             SocketChannel raw = SocketChannel.open(ss.getLocalAddress())) {
            TcpMessageChannel ch = track(TcpMessageChannel.wrap(ss.accept(), CFG));
            raw.write(ByteBuffer.allocate(64).putInt(2).put((byte) 'o').put((byte) 'k').putInt(CFG.maxFrame() + 1).flip());
            assertArrayEquals("ok".getBytes(), ch.poll(5_000));
            assertThrows(FrameException.class, () -> ch.poll(5_000));
            assertInstanceOf(FrameException.class, ch.failure());
            assertFalse(ch.isOpen());
            assertThrows(IllegalStateException.class, () -> ch.offer("x".getBytes()));
        }
    }

    @Test @Tag("part2") @Tag("io") @Tag("edge")
    void peerClosingMidFrameIsAnErrorButCompleteFramesSurvive() throws Exception {
        try (ServerSocketChannel ss = ServerSocketChannel.open().bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0))) {
            SocketChannel raw = SocketChannel.open(ss.getLocalAddress());
            TcpMessageChannel ch = track(TcpMessageChannel.wrap(ss.accept(), CFG));
            raw.write(ByteBuffer.allocate(64).putInt(3).put("abc".getBytes()).putInt(10).put("xyz".getBytes()).flip());
            raw.close();
            assertArrayEquals("abc".getBytes(), ch.poll(5_000));
            Await.until("channel closed", 5_000, () -> !ch.isOpen());
            assertInstanceOf(EOFException.class, ch.failure());
            assertNull(ch.poll());
            assertTrue(ch.isDrained());
        }
    }

    @Test @Tag("part2") @Tag("io")
    void finishSendingFlushesThenPeerSeesDrained() throws Exception {
        var p = pair(CFG);
        int n = 2_000;
        for (int i = 0; i < n; i++) assertTrue(p.client().offer(Await.msg(i), 10_000));
        p.client().finishSending();
        assertThrows(IllegalStateException.class, () -> p.client().offer("late".getBytes()));
        int got = 0;
        for (byte[] m; (m = p.server().poll(10_000)) != null; got++) assertTrue(Await.isMsg(m, got), "at " + got);
        assertEquals(n, got);                                       // 先收齐全部，poll 才会因为 EOF 返回 null
        assertTrue(p.server().isDrained());
        assertTrue(p.server().isPeerClosed());
        assertTrue(p.server().isOpen());                            // 半关闭：服务端还能回话
        assertTrue(p.server().offer("bye".getBytes()));
        assertArrayEquals("bye".getBytes(), p.client().poll(5_000));
        p.server().finishSending();                                 // 双方都结束 → 两端都关闭
        assertTrue(p.server().awaitClosed(5_000));
        assertTrue(p.client().awaitClosed(5_000));
        assertNull(p.client().failure());
        assertNull(p.server().failure());
    }

    @Test @Tag("part2") @Tag("io") @Tag("edge")
    void abruptCloseIsSeenByPeer() throws Exception {
        var p = pair(CFG);
        p.client().offer("last".getBytes());
        Await.until("flushed", 5_000, () -> p.client().unsentBytes() == 0);
        p.client().close();
        assertFalse(p.client().isOpen());
        assertThrows(IllegalStateException.class, () -> p.client().offer("x".getBytes()));
        assertArrayEquals("last".getBytes(), p.server().poll(5_000));
        Await.until("peer EOF seen", 5_000, () -> p.server().isPeerClosed());
        assertTrue(p.server().isDrained());
        p.client().close();                                         // 幂等
    }

    @Test @Tag("part2") @Tag("io") @Tag("edge")
    void closeWakesBlockedPollAndOffer() throws Exception {
        var p = pair(CFG);
        AtomicReference<Object> result = new AtomicReference<>("unset");
        Thread t = new Thread(() -> {
            try { result.set(p.server().poll(30_000)); } catch (Throwable e) { result.set(e); }
        });
        t.start();
        Thread.sleep(50);
        p.server().close();
        t.join(5_000);
        assertFalse(t.isAlive(), "poll(timeout) must return when the channel is closed");
        assertNull(result.get());
    }

    // ----------------------------------------------------------------------- Part 3

    /** 把发送缓冲 / 接收缓冲压到最小，让「内核缓冲区装满」在几十 KB 内发生。 */
    Pair tinyPair(ChannelConfig cfg) throws Exception {
        ServerSocketChannel ss = ServerSocketChannel.open();
        ss.setOption(StandardSocketOptions.SO_RCVBUF, 4096);
        ss.bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0));
        SocketChannel c = SocketChannel.open();
        c.setOption(StandardSocketOptions.SO_SNDBUF, 4096);
        c.connect(ss.getLocalAddress());
        SocketChannel s = ss.accept();
        ss.close();
        s.setOption(StandardSocketOptions.SO_RCVBUF, 4096);
        return new Pair(track(TcpMessageChannel.wrap(c, cfg)), track(TcpMessageChannel.wrap(s, cfg)));
    }

    @Test @Tag("part3") @Tag("io")
    void offerReturnsFalseWhenReceiverDoesNotReadThenRecoversWithoutLoss() throws Exception {
        ChannelConfig cfg = new ChannelConfig(256, 8 * 1024, 8 * 1024);
        var p = tinyPair(cfg);
        int accepted = 0;
        long limit = 2_000_000;
        // offer 返回 false 可能只是「I/O 线程还没来得及腾空间」；等 200ms 仍然放不下才算真的堵死（内核缓冲区 + 两端的环都满了）
        while (accepted < limit && p.client().offer(Await.msg(accepted), 200)) accepted++;
        assertTrue(accepted < limit, "outbound buffer is unbounded: " + accepted + " messages accepted without a reader");
        assertTrue(accepted > 0);
        assertFalse(p.client().offer(Await.msg(accepted), 20));    // 带超时的版本同样返回 false
        // 接收端开始读：之前接受的每一条都按顺序到达，没有丢、没有重
        for (int i = 0; i < accepted; i++) assertTrue(Await.isMsg(p.server().poll(10_000), i), "at " + i + " of " + accepted);
        assertNull(p.server().poll(50));
        // 缓冲区腾出来了，又能发
        assertTrue(p.client().offer(Await.msg(accepted), 5_000));
        assertTrue(Await.isMsg(p.server().poll(5_000), accepted));
    }

    @Test @Tag("part3") @Tag("io")
    void blockingOfferWaitsForSpaceAndSucceedsOnceReceiverReads() throws Exception {
        ChannelConfig cfg = new ChannelConfig(256, 4 * 1024, 4 * 1024);
        var p = tinyPair(cfg);
        int accepted = 0;
        while (accepted < 2_000_000 && p.client().offer(Await.msg(accepted), 200)) accepted++;
        int total = accepted;
        AtomicReference<Object> res = new AtomicReference<>();
        Thread blocked = new Thread(() -> {
            try { res.set(p.client().offer(Await.msg(total), 20_000)); } catch (Throwable t) { res.set(t); }
        });
        blocked.start();
        Thread.sleep(50);                                           // 不是正确性依赖：只是让它大概率先阻塞住
        for (int i = 0; i < total; i++) assertTrue(Await.isMsg(p.server().poll(10_000), i));
        blocked.join(10_000);
        assertEquals(Boolean.TRUE, res.get());
        assertTrue(Await.isMsg(p.server().poll(5_000), total));
    }

    /** 最小合法缓冲区（容量 = maxFrame + 4）：每条消息都在回绕边界上被切开，入站环经常是满的。 */
    @Test @Tag("part3") @Tag("io") @Tag("conc")
    void minimalBuffersStillDeliverEverythingInOrder() throws Exception {
        ChannelConfig cfg = new ChannelConfig(64, 68, 68);
        var p = tinyPair(cfg);
        int n = 20_000;
        AtomicReference<Throwable> err = new AtomicReference<>();
        Thread sender = new Thread(() -> {
            try { for (int i = 0; i < n; i++) assertTrue(p.client().offer(Await.msg(i), 20_000), "offer " + i); } catch (Throwable t) { err.compareAndSet(null, t); }
        });
        sender.start();
        for (int i = 0; i < n; i++) {
            byte[] m = p.server().poll(20_000);
            assertTrue(Await.isMsg(m, i), "message " + i + " wrong or missing");
        }
        sender.join(10_000);
        assertNull(err.get());
    }

    /** 非阻塞 poll() 自旋：入站环满 → I/O 线程停止监听 OP_READ；poll 腾出空间后必须把它叫醒，否则这里永远收不齐。 */
    @Test @Tag("part3") @Tag("io") @Tag("conc")
    void spinningNonBlockingPollResumesAPausedReader() throws Exception {
        ChannelConfig cfg = new ChannelConfig(64, 68, 68);
        var p = tinyPair(cfg);
        int n = 5_000;
        Thread sender = new Thread(() -> {
            try { for (int i = 0; i < n; i++) p.client().offer(Await.msg(i), 20_000); } catch (Exception e) { throw new RuntimeException(e); }
        });
        sender.start();
        long deadline = System.nanoTime() + 20_000_000_000L;
        int got = 0;
        while (got < n) {
            assertTrue(System.nanoTime() < deadline, "stalled after " + got + " messages");
            byte[] m = p.server().poll();
            if (m == null) { Thread.onSpinWait(); continue; }
            assertTrue(Await.isMsg(m, got), "at " + got);
            got++;
        }
        sender.join(10_000);
    }

    @Test @Tag("part3") @Tag("io") @Tag("edge")
    void slowReaderNeverMakesInboundBufferGrowBeyondItsBound() throws Exception {
        // 接收端每隔一阵才读一条：入站环只有 2 条消息大，发送端必须被拖慢而不是让内存增长
        ChannelConfig cfg = new ChannelConfig(64, 1024, 136);
        var p = tinyPair(cfg);
        int n = 3_000;
        AtomicReference<Throwable> err = new AtomicReference<>();
        Thread sender = new Thread(() -> {
            try { for (int i = 0; i < n; i++) assertTrue(p.client().offer(Await.msg(i), 30_000), "offer " + i); } catch (Throwable t) { err.compareAndSet(null, t); }
        });
        sender.start();
        for (int i = 0; i < n; i++) {
            if (i % 500 == 0) Thread.sleep(20);
            assertTrue(Await.isMsg(p.server().poll(30_000), i), "at " + i);
        }
        sender.join(10_000);
        assertNull(err.get());
    }
}
