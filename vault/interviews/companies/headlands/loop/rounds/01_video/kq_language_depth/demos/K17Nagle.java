import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.Iterator;

/**
 * Single-threaded NIO Selector server (reads a 2-part request: 4-byte header then 4-byte body, replies 1 byte)
 * vs a blocking client that sends the two parts in two writes.  Measures round trip with Nagle on / off.
 */
public class K17Nagle {
    public static void main(String[] a) throws Exception {
        ServerSocketChannel ssc = ServerSocketChannel.open().bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0));
        ssc.configureBlocking(false);
        Selector sel = Selector.open(); ssc.register(sel, SelectionKey.OP_ACCEPT);
        int port = ((InetSocketAddress) ssc.getLocalAddress()).getPort();
        Thread server = new Thread(() -> {
            try {
                ByteBuffer buf = ByteBuffer.allocateDirect(64);
                while (sel.isOpen()) {
                    sel.select(); Iterator<SelectionKey> it = sel.selectedKeys().iterator();
                    while (it.hasNext()) {
                        SelectionKey k = it.next(); it.remove();
                        if (k.isAcceptable()) { SocketChannel c = ssc.accept(); c.configureBlocking(false); c.setOption(StandardSocketOptions.TCP_NODELAY, true); c.register(sel, SelectionKey.OP_READ, new int[1]); }
                        else if (k.isReadable()) {
                            SocketChannel c = (SocketChannel) k.channel(); int[] got = (int[]) k.attachment(); buf.clear();
                            int n = c.read(buf); if (n < 0) { c.close(); continue; }
                            got[0] += n;
                            if (got[0] >= 8) { got[0] -= 8; c.write(ByteBuffer.wrap(new byte[]{1})); }
                        }
                    }
                }
            } catch (ClosedSelectorException | IOException e) { }
        }, "selector-server");
        server.setDaemon(true); server.start();
        for (boolean noDelay : new boolean[]{true, false}) {
            try (Socket s = new Socket(InetAddress.getLoopbackAddress(), port)) {
                s.setTcpNoDelay(noDelay);
                var out = s.getOutputStream(); var in = s.getInputStream(); byte[] part = new byte[4];
                int n = noDelay ? 20_000 : 200;
                for (int i = 0; i < 20; i++) { out.write(part); out.flush(); out.write(part); out.flush(); in.read(); }
                long t0 = System.nanoTime();
                for (int i = 0; i < n; i++) { out.write(part); out.flush(); out.write(part); out.flush(); in.read(); }
                System.out.printf("TCP_NODELAY=%-5b two small writes then wait: %9.1f us per request (n=%d)%n", noDelay, (System.nanoTime() - t0) / 1000.0 / n, n);
            }
        }
        sel.close();
    }
}
