import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

/**
 * 监听一个端口，把每个新连接包成 TcpMessageChannel 放进队列，由 accept(timeout) 取走。
 * 只做本题需要的最小功能：一个接受线程 + 阻塞 accept；port 传 0 = 让内核选临时端口（测试用）。
 */
public final class MessageServer implements AutoCloseable {
    private final ServerSocketChannel server;
    private final ChannelConfig cfg;
    private final BlockingQueue<TcpMessageChannel> accepted = new LinkedBlockingQueue<>();
    private volatile boolean closed;

    public MessageServer(int port, ChannelConfig cfg) throws IOException {
        this.cfg = cfg;
        this.server = ServerSocketChannel.open();
        try {
            server.bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), port));
        } catch (IOException | RuntimeException e) {
            server.close();
            throw e;
        }
        Thread t = new Thread(this::acceptLoop, "msg-server-accept-" + port());
        t.setDaemon(true);
        t.start();
    }

    public int port() { return ((InetSocketAddress) serverAddress()).getPort(); }

    public InetSocketAddress address() { return (InetSocketAddress) serverAddress(); }

    private java.net.SocketAddress serverAddress() {
        try { return server.getLocalAddress(); } catch (IOException e) { throw new IllegalStateException(e); }
    }

    /** 等下一个连接；超时返回 null。 */
    public TcpMessageChannel accept(long timeoutMs) throws InterruptedException {
        return accepted.poll(timeoutMs, TimeUnit.MILLISECONDS);
    }

    private void acceptLoop() {
        while (!closed) {
            try {
                SocketChannel sc = server.accept();
                try {
                    accepted.add(TcpMessageChannel.wrap(sc, cfg));
                } catch (IOException | RuntimeException e) {
                    try { sc.close(); } catch (IOException ignored) { }
                }
            } catch (IOException e) {
                return;      // 服务端被关闭
            }
        }
    }

    @Override
    public void close() {
        closed = true;
        try { server.close(); } catch (IOException ignored) { }
        TcpMessageChannel c;
        while ((c = accepted.poll()) != null) c.close();         // 没人取走的连接一并关掉
    }
}
