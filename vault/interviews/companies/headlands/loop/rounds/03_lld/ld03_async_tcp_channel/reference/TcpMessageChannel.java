import java.io.EOFException;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.SocketAddress;
import java.net.StandardSocketOptions;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Part 2/3：一条 TCP 连接上的「有界消息通道」。
 *
 * <pre>
 *   app 线程                                    I/O 线程（一个 Selector）
 *   offer(msg) ─encode─▶ [out 环] ──读出──▶ wbuf ──ch.write──▶ socket ─▶ 网络
 *   poll()    ◀─decode── [in 环]  ◀─feed──  rbuf ◀─ch.read──  socket ◀─ 网络
 * </pre>
 *
 * 语义要点：
 * <ul>
 *   <li>offer 不阻塞：out 环放不下一整帧就返回 false（背压交给调用方）。已接受的消息保证按顺序写进 socket，除非连接失败。</li>
 *   <li>入站背压：in 环满了，I/O 线程停止监听 OP_READ，不再从内核取数据；内核接收缓冲区填满 → TCP 窗口缩到 0 → 对端写不出去。</li>
 *   <li>部分 I/O：write 可能只写一部分（留在 wbuf 里等 OP_WRITE），read 可能只收到半条消息（留在 in 环里等后续字节）。</li>
 *   <li>对端关闭（EOF）≠ 本端关闭：peerClosed 之后仍可 poll 剩余的完整消息、仍可 offer；isDrained() 表示「再也不会有新消息了」。</li>
 *   <li>finishSending()：停止接受 offer，刷完后发 FIN（半关闭）；双方都结束后通道关闭。close()：立刻关。</li>
 * </ul>
 * 所有可变状态由一把 ReentrantLock 保护（临界区只做内存拷贝，不做 I/O）；系统调用都在锁外。
 * 想要无锁版本见 ld01 的 SPSC 环——这里的瓶颈是系统调用，不是这把锁。
 */
public final class TcpMessageChannel implements AutoCloseable {
    private enum State { OPEN, FINISHING, CLOSED }

    private static final int IO_BUF = 16 * 1024;

    private final SocketChannel ch;
    private final Selector selector;
    private final SelectionKey key;
    private final ChannelConfig cfg;

    private final ReentrantLock lock = new ReentrantLock();
    private final Condition changed = lock.newCondition();
    private final ByteRing out;
    private final FrameDecoder in;
    private final ByteBuffer wbuf = ByteBuffer.allocateDirect(IO_BUF);
    private final ByteBuffer rbuf = ByteBuffer.allocateDirect(IO_BUF);

    private State state = State.OPEN;
    private boolean peerClosed;
    private boolean finSent;
    private boolean readPaused;
    private Throwable failure;
    private final Thread ioThread;

    /** 阻塞地连接（最多 timeoutMs），成功后切到非阻塞并启动 I/O 线程。 */
    public static TcpMessageChannel connect(InetSocketAddress addr, ChannelConfig cfg, int timeoutMs) throws IOException {
        SocketChannel sc = SocketChannel.open();
        try {
            sc.socket().connect(addr, timeoutMs);
            return new TcpMessageChannel(sc, cfg);
        } catch (IOException | RuntimeException e) {
            try { sc.close(); } catch (IOException suppressed) { e.addSuppressed(suppressed); }
            throw e;
        }
    }

    public static TcpMessageChannel connect(InetSocketAddress addr, ChannelConfig cfg) throws IOException {
        return connect(addr, cfg, 3_000);
    }

    /** 接管一个已经连接好的 SocketChannel（服务端 accept 出来的，或测试里调过 SO_SNDBUF 的）。 */
    public static TcpMessageChannel wrap(SocketChannel connected, ChannelConfig cfg) throws IOException {
        return new TcpMessageChannel(connected, cfg);
    }

    private TcpMessageChannel(SocketChannel sc, ChannelConfig cfg) throws IOException {
        this.cfg = java.util.Objects.requireNonNull(cfg, "cfg");
        this.ch = sc;
        Selector sel = null;
        try {
            sc.configureBlocking(false);
            sc.setOption(StandardSocketOptions.TCP_NODELAY, true);      // 小消息别等 Nagle（见 networking_basics §5）
            sel = Selector.open();
            this.selector = sel;
            this.key = sc.register(sel, 0);
        } catch (IOException | RuntimeException e) {
            if (sel != null) sel.close();
            throw e;
        }
        this.out = new ByteRing(cfg.outCapacity());
        this.in = new FrameDecoder(cfg.maxFrame(), cfg.inCapacity());
        wbuf.limit(0);
        this.ioThread = new Thread(this::ioLoop, "tcp-io-" + sc.getLocalAddress());
        this.ioThread.setDaemon(true);
        this.ioThread.start();
    }

    // ------------------------------------------------------------------ 应用线程 API

    /**
     * 非阻塞发送。
     * @return true = 已进入出站缓冲区；false = 缓冲区满（稍后重试，这就是背压）
     * @throws IllegalArgumentException 消息超过 maxFrame
     * @throws IllegalStateException    通道已关闭 / 已 finishSending（原因见 failure()）
     */
    public boolean offer(byte[] msg) {
        lock.lock();
        boolean wasEmpty;
        try {
            requireSendable();
            wasEmpty = out.isEmpty();
            if (!FrameCodec.encode(out, msg, cfg.maxFrame())) return false;
        } finally {
            lock.unlock();
        }
        if (wasEmpty) selector.wakeup();     // out 非空时 I/O 线程已经在等 OP_WRITE，不必再唤醒
        return true;
    }

    /** 最多等 timeoutMs 毫秒直到放得下。 */
    public boolean offer(byte[] msg, long timeoutMs) throws InterruptedException {
        long nanos = TimeUnit.MILLISECONDS.toNanos(timeoutMs);
        lock.lock();
        try {
            for (;;) {
                requireSendable();
                boolean wasEmpty = out.isEmpty();
                if (FrameCodec.encode(out, msg, cfg.maxFrame())) {
                    if (wasEmpty) selector.wakeup();
                    return true;
                }
                if (nanos <= 0) return false;
                nanos = changed.awaitNanos(nanos);
            }
        } finally {
            lock.unlock();
        }
    }

    /** 下一条完整消息，没有返回 null。即使通道已关闭，已缓冲的完整消息仍然可取。 */
    public byte[] poll() {
        boolean wake;
        byte[] m;
        lock.lock();
        try {
            m = nextLocked();
            wake = m != null && readPaused;
            if (wake) readPaused = false;
        } finally {
            lock.unlock();
        }
        if (wake) selector.wakeup();
        return m;
    }

    /** 等到有消息、或不会再有消息（drained）、或超时。 */
    public byte[] poll(long timeoutMs) throws InterruptedException {
        long nanos = TimeUnit.MILLISECONDS.toNanos(timeoutMs);
        boolean wake = false;
        byte[] m;
        lock.lock();
        try {
            for (;;) {
                m = nextLocked();
                if (m != null || inboundFinishedLocked() || nanos <= 0) break;
                nanos = changed.awaitNanos(nanos);
            }
            if (m != null && readPaused) { readPaused = false; wake = true; }
        } finally {
            lock.unlock();
        }
        if (wake) selector.wakeup();
        return m;
    }

    /** 不再接受 offer；已接受的消息刷完后发 FIN。对端也结束后通道关闭。 */
    public void finishSending() {
        lock.lock();
        try {
            if (state == State.OPEN) state = State.FINISHING;
        } finally {
            lock.unlock();
        }
        selector.wakeup();
    }

    /** 立刻关闭，丢弃未发送的数据。幂等。 */
    @Override
    public void close() {
        lock.lock();
        try {
            state = State.CLOSED;
            changed.signalAll();
        } finally {
            lock.unlock();
        }
        selector.wakeup();
        if (Thread.currentThread() != ioThread) {
            try { ioThread.join(2_000); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        }
    }

    public boolean isOpen() { return locked(() -> state != State.CLOSED); }

    public boolean isPeerClosed() { return locked(() -> peerClosed); }

    /** 不会再有新消息了（对端已关闭或本端已关闭）且缓冲区里没有完整的消息了。 */
    public boolean isDrained() { return locked(() -> inboundFinishedLocked() && !in.hasFrame()); }

    /** 因错误而关闭时的原因；正常关闭 / 仍打开为 null。 */
    public Throwable failure() { return locked(() -> failure); }

    /** 已接受但尚未写进 socket 的字节数（出站环 + wbuf）。 */
    public int unsentBytes() { return locked(() -> out.size() + wbuf.remaining()); }

    public boolean awaitClosed(long timeoutMs) throws InterruptedException {
        long nanos = TimeUnit.MILLISECONDS.toNanos(timeoutMs);
        lock.lock();
        try {
            while (state != State.CLOSED) {
                if (nanos <= 0) return false;
                nanos = changed.awaitNanos(nanos);
            }
            return true;
        } finally {
            lock.unlock();
        }
    }

    public InetSocketAddress localAddress() throws IOException { return (InetSocketAddress) ch.getLocalAddress(); }

    public SocketAddress remoteAddress() throws IOException { return ch.getRemoteAddress(); }

    // ------------------------------------------------------------------ 内部（持锁）

    private byte[] nextLocked() {
        try {
            return in.next();
        } catch (FrameException e) {
            failLocked(e);
            throw e;
        }
    }

    private boolean inboundFinishedLocked() { return peerClosed || state == State.CLOSED; }

    private void requireSendable() {
        if (state != State.OPEN) {
            throw new IllegalStateException(state == State.FINISHING ? "finishSending() was called" : "channel closed", failure);
        }
    }

    private void failLocked(Throwable t) {
        if (failure == null) failure = t;
        state = State.CLOSED;
        changed.signalAll();
    }

    private <T> T locked(java.util.function.Supplier<T> s) {
        lock.lock();
        try { return s.get(); } finally { lock.unlock(); }
    }

    private boolean locked(java.util.function.BooleanSupplier s) {
        lock.lock();
        try { return s.getAsBoolean(); } finally { lock.unlock(); }
    }

    // ------------------------------------------------------------------ I/O 线程

    private void ioLoop() {
        try {
            for (;;) {
                int ops = 0;
                lock.lock();
                try {
                    if (state == State.CLOSED) break;
                    if (state == State.FINISHING && !finSent && out.isEmpty() && !wbuf.hasRemaining()) {
                        ch.shutdownOutput();                         // 发 FIN：对端 read 返回 -1
                        finSent = true;
                    }
                    if (finSent && peerClosed) { state = State.CLOSED; changed.signalAll(); break; }
                    readPaused = !peerClosed && in.free() == 0;
                    if (!peerClosed && in.free() > 0) ops |= SelectionKey.OP_READ;
                    if (!finSent && (wbuf.hasRemaining() || !out.isEmpty())) ops |= SelectionKey.OP_WRITE;
                } finally {
                    lock.unlock();
                }
                key.interestOps(ops);
                selector.select();                                   // 睡到：socket 就绪 或 selector.wakeup()
                if (selector.selectedKeys().remove(key)) {           // 只在本轮真的被选中时才看 readyOps（否则是上一轮的旧值）
                    if (key.isReadable()) doRead();
                    if (key.isWritable()) doWrite();
                }
            }
        } catch (Throwable t) {
            lock.lock();
            try { failLocked(t); } finally { lock.unlock(); }
        } finally {
            try { ch.close(); } catch (IOException ignored) { }
            try { selector.close(); } catch (IOException ignored) { }
            lock.lock();
            try { state = State.CLOSED; changed.signalAll(); } finally { lock.unlock(); }
        }
    }

    private void doRead() throws IOException {
        int room;
        lock.lock();
        try { room = in.free(); } finally { lock.unlock(); }
        if (room == 0) return;
        rbuf.clear();
        rbuf.limit(Math.min(rbuf.capacity(), room));
        int n = ch.read(rbuf);
        if (n < 0) {
            lock.lock();
            try {
                peerClosed = true;
                if (in.hasTruncatedTail()) failLocked(new EOFException("peer closed in the middle of a frame (" + in.buffered() + " bytes buffered)"));
                changed.signalAll();
            } finally {
                lock.unlock();
            }
        } else if (n > 0) {
            rbuf.flip();
            lock.lock();
            try {
                in.feed(rbuf);                                       // room >= n：一定吃得下
                changed.signalAll();
            } finally {
                lock.unlock();
            }
        }
    }

    private void doWrite() throws IOException {
        for (int round = 0; round < 16; round++) {                   // 限制一轮最多写多少，别饿死读
            if (!wbuf.hasRemaining()) {
                lock.lock();
                try {
                    wbuf.clear();
                    out.read(wbuf);
                    wbuf.flip();
                    changed.signalAll();                             // out 腾出了空间：唤醒阻塞在 offer(msg, timeout) 的线程
                } finally {
                    lock.unlock();
                }
                if (!wbuf.hasRemaining()) return;
            }
            int n = ch.write(wbuf);                                  // 可能只写一部分，剩下的留在 wbuf 里，等下一次 OP_WRITE
            if (n == 0) return;
        }
    }
}
