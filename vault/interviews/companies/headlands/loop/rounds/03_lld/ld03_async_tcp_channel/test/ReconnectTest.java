import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.channels.ServerSocketChannel;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 4：指数退避 + 自动重连。 */
class ReconnectTest {
    static final ChannelConfig CFG = new ChannelConfig(256, 4 * 1024, 4 * 1024);

    private final List<AutoCloseable> toClose = new ArrayList<>();

    <T extends AutoCloseable> T track(T c) { toClose.add(c); return c; }

    @AfterEach
    void cleanup() throws Exception { for (AutoCloseable c : toClose) c.close(); }

    // ---------------------------------------------------------------- Backoff

    @Test @Tag("part4")
    void backoffDoublesUpToCapThenStaysThere() {
        Backoff b = new Backoff(100, 1_000, 2);
        long[] expected = {100, 200, 400, 800, 1_000, 1_000, 1_000};
        for (long e : expected) assertEquals(e, b.next());
    }

    @Test @Tag("part4")
    void backoffResetStartsOver() {
        Backoff b = new Backoff(5, 100, 3);
        assertEquals(5, b.next()); assertEquals(15, b.next()); assertEquals(45, b.next()); assertEquals(100, b.next());
        b.reset();
        assertEquals(5, b.next());
    }

    @Test @Tag("part4") @Tag("edge")
    void backoffCapsExactlyAndNeverOverflows() {
        Backoff b = new Backoff(1, Long.MAX_VALUE, 10);
        long prev = 0;
        for (int i = 0; i < 100; i++) {
            long d = b.next();
            assertTrue(d >= prev && d > 0, "step " + i + " -> " + d);
            prev = d;
        }
        assertEquals(Long.MAX_VALUE, prev);
        Backoff c = new Backoff(7, 7, 2);
        assertEquals(7, c.next()); assertEquals(7, c.next());
        Backoff flat = new Backoff(10, 1_000, 1);
        for (int i = 0; i < 5; i++) assertEquals(10, flat.next());
    }

    @Test @Tag("part4") @Tag("edge")
    void backoffFullJitterStaysWithinZeroAndCurrentCap() {
        Random rnd = new Random(42);
        Backoff b = new Backoff(10, 80, 2);
        long[] caps = {10, 20, 40, 80, 80, 80};
        boolean sawNonCap = false;
        for (long cap : caps) {
            long d = b.next(rnd);
            assertTrue(d >= 0 && d <= cap, d + " not in [0," + cap + "]");
            if (d != cap) sawNonCap = true;
        }
        assertTrue(sawNonCap);
    }

    @Test @Tag("part4") @Tag("edge")
    void backoffRejectsBadParameters() {
        assertThrows(IllegalArgumentException.class, () -> new Backoff(0, 10, 2));
        assertThrows(IllegalArgumentException.class, () -> new Backoff(10, 5, 2));
        assertThrows(IllegalArgumentException.class, () -> new Backoff(1, 10, 0));
    }

    // ---------------------------------------------------------------- ReconnectingClient

    @Test @Tag("part4") @Tag("io")
    void reconnectsAfterServerDropsTheConnection() throws Exception {
        MessageServer srv = track(new MessageServer(0, CFG));
        ReconnectingClient client = track(new ReconnectingClient(srv.address(), CFG, new Backoff(2, 50, 2)));
        TcpMessageChannel first = srv.accept(5_000);
        assertNotNull(first);
        assertTrue(client.offer("one".getBytes()));
        assertArrayEquals("one".getBytes(), first.poll(5_000));
        assertEquals(1, client.connectCount());

        first.close();                                                   // 服务端主动断开
        TcpMessageChannel second = srv.accept(5_000);                    // 客户端自己重连了
        assertNotNull(second, "client did not reconnect");
        Await.until("client sees second connection", 5_000, () -> client.connectCount() == 2 && client.isConnected());
        assertTrue(client.offer("two".getBytes()));
        assertArrayEquals("two".getBytes(), second.poll(5_000));
        // 反方向也通
        assertTrue(second.offer("pong".getBytes()));
        Await.until("inbound on new connection", 5_000, () -> {
            byte[] m = client.poll();
            return m != null && new String(m).equals("pong");
        });
    }

    @Test @Tag("part4") @Tag("io")
    void messagesOfferedWhileServerIsDownAreDeliveredInOrderAfterItComesBack() throws Exception {
        MessageServer srv1 = new MessageServer(0, CFG);
        int port = srv1.port();
        ReconnectingClient client = track(new ReconnectingClient(srv1.address(), CFG, new Backoff(2, 20, 2)));
        TcpMessageChannel c1 = srv1.accept(5_000);
        assertTrue(client.offer("before".getBytes()));
        assertArrayEquals("before".getBytes(), c1.poll(5_000));

        c1.close();
        srv1.close();                                                    // 服务端整个下线：端口不再监听
        Await.until("client notices the disconnect", 5_000, () -> !client.isConnected());
        for (int i = 0; i < 5; i++) assertTrue(client.offer(Await.msg(i)), "offer while disconnected must be accepted");
        Await.until("client retried and failed", 5_000, () -> client.failedAttempts() >= 3);
        assertTrue(client.pendingBytes() > 0);

        MessageServer srv2 = track(new MessageServer(port, CFG));         // 同一个端口重新上线
        TcpMessageChannel c2 = srv2.accept(10_000);
        assertNotNull(c2, "client did not reconnect to the restarted server");
        for (int i = 0; i < 5; i++) assertTrue(Await.isMsg(c2.poll(5_000), i), "message " + i);
        assertNull(c2.poll(50));
        Await.until("pending drained", 5_000, () -> client.pendingBytes() == 0);
    }

    @Test @Tag("part4") @Tag("io") @Tag("edge")
    void pendingQueueIsBoundedWhileDisconnected() throws Exception {
        int port;
        try (ServerSocketChannel probe = ServerSocketChannel.open().bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0))) {
            port = ((InetSocketAddress) probe.getLocalAddress()).getPort();
        }                                                                // 关掉：这个端口现在没人监听
        ChannelConfig small = new ChannelConfig(100, 500, 500);
        ReconnectingClient client = track(new ReconnectingClient(new InetSocketAddress(InetAddress.getLoopbackAddress(), port), small, new Backoff(5, 20, 2)));
        int accepted = 0;
        while (client.offer(new byte[46])) accepted++;                   // 每条编码后 50 字节 → 容量 500 装 10 条
        assertEquals(10, accepted);
        assertEquals(500, client.pendingBytes());
        assertFalse(client.offer(new byte[0]));                           // 4 字节也放不下
        assertThrows(IllegalArgumentException.class, () -> client.offer(new byte[101]));
        Await.until("keeps retrying", 5_000, () -> client.failedAttempts() >= 3);
        assertFalse(client.isConnected());
        assertNull(client.poll());
    }

    @Test @Tag("part4") @Tag("io") @Tag("edge")
    void closeStopsReconnectingAndRejectsOffers() throws Exception {
        MessageServer srv = track(new MessageServer(0, CFG));
        ReconnectingClient client = new ReconnectingClient(srv.address(), CFG, new Backoff(2, 10, 2));
        TcpMessageChannel c = srv.accept(5_000);
        assertNotNull(c);
        client.close();
        assertThrows(IllegalStateException.class, () -> client.offer("x".getBytes()));
        Await.until("server sees EOF", 5_000, () -> c.isPeerClosed());
        int count = client.connectCount();
        assertNull(srv.accept(150), "a closed client must not reconnect");
        assertEquals(count, client.connectCount());
        client.close();                                                  // 幂等
    }

    @Test @Tag("part4") @Tag("io") @Tag("edge")
    void backoffResetsAfterSuccessfulConnect() throws Exception {
        // 先让客户端失败几次（没有服务器），再上线；上线后又被踢掉，重连应当很快（退避已重置）
        int port;
        try (ServerSocketChannel probe = ServerSocketChannel.open().bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0))) {
            port = ((InetSocketAddress) probe.getLocalAddress()).getPort();
        }
        ReconnectingClient client = track(new ReconnectingClient(new InetSocketAddress(InetAddress.getLoopbackAddress(), port), CFG, new Backoff(5, 2_000, 4)));
        Await.until("failed a few times", 5_000, () -> client.failedAttempts() >= 3);
        MessageServer srv = track(new MessageServer(port, CFG));
        TcpMessageChannel c1 = srv.accept(10_000);
        assertNotNull(c1);
        c1.close();
        long t0 = System.nanoTime();
        TcpMessageChannel c2 = srv.accept(1_500);                         // 若退避没重置，这里要等 >= 320ms 乃至 2s
        assertNotNull(c2, "reconnect after a successful session should start from the initial delay");
        assertTrue((System.nanoTime() - t0) < 1_500_000_000L);
    }
}
