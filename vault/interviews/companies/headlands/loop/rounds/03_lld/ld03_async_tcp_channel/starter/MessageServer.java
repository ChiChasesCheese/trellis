import java.io.IOException;
import java.net.InetSocketAddress;

/** 监听 127.0.0.1:port（0 = 临时端口），把每个新连接包成 TcpMessageChannel 放进队列，由 accept(timeout) 取走。 */
public final class MessageServer implements AutoCloseable {
    public MessageServer(int port, ChannelConfig cfg) throws IOException {
        throw new UnsupportedOperationException("TODO");
    }

    public int port() { throw new UnsupportedOperationException("TODO"); }

    public InetSocketAddress address() { throw new UnsupportedOperationException("TODO"); }

    /** 等下一个连接；超时返回 null。 */
    public TcpMessageChannel accept(long timeoutMs) throws InterruptedException { throw new UnsupportedOperationException("TODO"); }

    /** 关闭监听；没人取走的连接一并关掉。 */
    @Override
    public void close() { throw new UnsupportedOperationException("TODO"); }
}
