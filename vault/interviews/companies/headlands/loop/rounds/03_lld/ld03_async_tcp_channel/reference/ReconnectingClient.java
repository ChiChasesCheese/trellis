import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.ArrayDeque;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Part 4b：自动重连的客户端。
 *
 * <pre>
 *   offer(msg) ─▶ [pending 队列，有界] ──管理线程──▶ 当前 TcpMessageChannel ─▶ 网络
 *                                         │ 连接失败 / 对端关闭：指数退避后重连，pending 里的消息留着等新连接
 * </pre>
 * 语义（务必说清楚，这是面试官要听的）：
 * <ul>
 *   <li>断线期间 offer 仍然成功（进 pending，直到装满为止，满了返回 false）；重连后按原顺序发出。</li>
 *   <li>已经交给旧通道（进了它的出站缓冲区 / 内核缓冲区）的消息，连接断掉时<b>可能丢失</b>——TCP 只保证「连接存续期间」有序不丢，
 *       不保证对端应用已经处理。要不丢，需要应用层序号 + 确认 + 重传（at-least-once + 去重）；本类是 at-most-once 的「尽力而为」。
 *       丢失的字节数累计在 abandonedBytes()。</li>
 *   <li>重连后旧通道里没来得及 poll 的入站消息被丢弃（新连接是新的字节流，协议要自己处理续传）。</li>
 * </ul>
 * 管理线程是一条虚拟线程（J10）：里面全是阻塞调用（connect、条件等待），写成直线代码最清楚。
 */
public final class ReconnectingClient implements AutoCloseable {
    private final InetSocketAddress addr;
    private final ChannelConfig cfg;
    private final Backoff backoff;

    private final ReentrantLock lock = new ReentrantLock();
    private final Condition wake = lock.newCondition();
    private final ArrayDeque<byte[]> pending = new ArrayDeque<>();
    private int pendingBytes;                        // 已编码大小：4 + len 之和，与出站环同一口径
    private TcpMessageChannel current;
    private boolean closed;
    private int connectCount;
    private int failedAttempts;
    private long abandonedBytes;
    private final Thread manager;

    public ReconnectingClient(InetSocketAddress addr, ChannelConfig cfg, Backoff backoff) {
        this.addr = java.util.Objects.requireNonNull(addr);
        this.cfg = java.util.Objects.requireNonNull(cfg);
        this.backoff = java.util.Objects.requireNonNull(backoff);
        this.manager = Thread.ofVirtual().name("reconnecting-client-" + addr).start(this::run);
    }

    /** @return true = 已接受（在 pending 或已交给通道）；false = pending 满了。 */
    public boolean offer(byte[] msg) {
        java.util.Objects.requireNonNull(msg, "msg");
        if (msg.length > cfg.maxFrame()) throw new IllegalArgumentException("message larger than maxFrame");
        int framed = FrameCodec.HEADER + msg.length;
        lock.lock();
        try {
            if (closed) throw new IllegalStateException("client closed");
            if (pendingBytes + framed > cfg.outCapacity()) return false;
            pending.addLast(msg);
            pendingBytes += framed;
            wake.signalAll();
            return true;
        } finally {
            lock.unlock();
        }
    }

    /** 当前连接上的下一条入站消息；断线期间返回 null。 */
    public byte[] poll() {
        TcpMessageChannel c;
        lock.lock();
        try { c = current; } finally { lock.unlock(); }
        return c == null ? null : c.poll();
    }

    public boolean isConnected() { return lockedGet(() -> current != null); }
    public int connectCount() { return lockedGet(() -> connectCount); }
    public int failedAttempts() { return lockedGet(() -> failedAttempts); }
    public long abandonedBytes() { return lockedGet(() -> abandonedBytes); }
    public int pendingBytes() { return lockedGet(() -> pendingBytes); }

    @Override
    public void close() {
        TcpMessageChannel c;
        lock.lock();
        try {
            closed = true;
            c = current;
            wake.signalAll();
        } finally {
            lock.unlock();
        }
        if (c != null) c.close();
        try { manager.join(3_000); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
    }

    private <T> T lockedGet(java.util.function.Supplier<T> s) {
        lock.lock();
        try { return s.get(); } finally { lock.unlock(); }
    }

    private void run() {
        while (!isClosed()) {
            TcpMessageChannel ch;
            try {
                ch = TcpMessageChannel.connect(addr, cfg, 2_000);
            } catch (IOException e) {
                lock.lock();
                try { failedAttempts++; } finally { lock.unlock(); }
                if (!sleep(backoff.next())) return;
                continue;
            }
            lock.lock();
            try {
                if (closed) { ch.close(); return; }
                current = ch;
                connectCount++;
                backoff.reset();
            } finally {
                lock.unlock();
            }
            pump(ch);
            lock.lock();
            try {
                current = null;
                abandonedBytes += ch.unsentBytes();
            } finally {
                lock.unlock();
            }
            ch.close();
        }
    }

    /** 把 pending 搬进通道，直到通道不可用或客户端关闭。 */
    private void pump(TcpMessageChannel ch) {
        lock.lock();
        try {
            while (!closed && ch.isOpen() && !ch.isPeerClosed()) {
                while (!pending.isEmpty()) {
                    byte[] m = pending.peekFirst();
                    boolean accepted;
                    try {
                        accepted = ch.offer(m);
                    } catch (IllegalStateException channelDied) {
                        return;
                    }
                    if (!accepted) break;                // 通道的出站环满了：等一会儿再试
                    pending.pollFirst();
                    pendingBytes -= FrameCodec.HEADER + m.length;
                }
                try {
                    wake.await(10, TimeUnit.MILLISECONDS);   // 周期性醒来检查连接是否还活着 / 出站环是否腾出了空间
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        } finally {
            lock.unlock();
        }
    }

    private boolean isClosed() { return lockedGet(() -> closed); }

    /** 可被 close() 打断的睡眠。@return false = 客户端已关闭 */
    private boolean sleep(long ms) {
        lock.lock();
        try {
            long nanos = TimeUnit.MILLISECONDS.toNanos(ms);
            while (!closed && nanos > 0) nanos = wake.awaitNanos(nanos);
            return !closed;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        } finally {
            lock.unlock();
        }
    }
}
