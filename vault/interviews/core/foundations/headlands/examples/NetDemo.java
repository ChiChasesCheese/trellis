import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.StandardProtocolFamily;
import java.net.StandardSocketOptions;
import java.nio.ByteBuffer;
import java.nio.channels.DatagramChannel;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import java.util.ArrayList;
import java.util.List;

/**
 * Companion to networking_basics.md. Everything runs on the loopback interface of one machine, so
 * numbers show software/kernel overhead, NOT wire latency.
 * Run:  javac --release 21 --enable-preview NetDemo.java && java --enable-preview NetDemo
 */
public class NetDemo {

    // ---------- servers: both echo every byte back ---------------------------------------------------

    /** One thread, one Selector, many connections (classic NIO reactor). Returns the bound port. */
    static int startSelectorEcho() throws IOException {
        ServerSocketChannel server = ServerSocketChannel.open();
        server.bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 1024);
        server.configureBlocking(false);
        Selector selector = Selector.open();
        server.register(selector, SelectionKey.OP_ACCEPT);
        Thread t = new Thread(() -> {
            ByteBuffer buf = ByteBuffer.allocateDirect(4096);
            try {
                while (true) {
                    selector.select();                                   // sleeps in the kernel (kqueue / epoll) until something is ready
                    Iterator<SelectionKey> it = selector.selectedKeys().iterator();
                    while (it.hasNext()) {
                        SelectionKey key = it.next();
                        it.remove();
                        if (key.isAcceptable()) {
                            SocketChannel c = server.accept();
                            if (c == null) continue;
                            c.configureBlocking(false);
                            c.setOption(StandardSocketOptions.TCP_NODELAY, true);
                            c.register(selector, SelectionKey.OP_READ);
                        } else if (key.isReadable()) {
                            SocketChannel c = (SocketChannel) key.channel();
                            buf.clear();
                            int n = c.read(buf);
                            if (n < 0) { key.cancel(); c.close(); continue; }
                            buf.flip();
                            while (buf.hasRemaining()) c.write(buf);     // tiny messages: assume the socket buffer has room
                        }
                    }
                }
            } catch (IOException e) { /* demo: ignore */ }
        }, "selector-echo");
        t.setDaemon(true);
        t.start();
        return ((InetSocketAddress) server.getLocalAddress()).getPort();
    }

    /** Thread-per-connection with plain blocking I/O, each connection on its own virtual thread. */
    static int startVirtualThreadEcho() throws IOException {
        ServerSocket server = new ServerSocket(0, 1024, InetAddress.getLoopbackAddress());
        Thread acceptor = new Thread(() -> {
            try (ExecutorService pool = Executors.newVirtualThreadPerTaskExecutor()) {
                while (true) {
                    Socket s = server.accept();
                    pool.submit(() -> {
                        try (s; InputStream in = s.getInputStream(); OutputStream out = s.getOutputStream()) {
                            s.setTcpNoDelay(true);
                            byte[] b = new byte[4096];
                            int n;
                            while ((n = in.read(b)) > 0) { out.write(b, 0, n); }   // blocking calls: the virtual thread parks, the carrier thread is freed
                        } catch (IOException e) { /* connection closed */ }
                        return null;
                    });
                }
            } catch (IOException e) { /* demo: ignore */ }
        }, "vt-acceptor");
        acceptor.setDaemon(true);
        acceptor.start();
        return server.getLocalPort();
    }

    public static void main(String[] args) throws Exception {
        nagle();
        concurrentClients();
        multicast();
    }

    // ---------- 1. Nagle's algorithm + delayed ACK: write-write-read ---------------------------------
    static void nagle() throws Exception {
        System.out.println("== 1. request sent as two small writes (header, then body), then wait for the reply ==");
        int port = startSelectorEcho();
        for (boolean nodelay : new boolean[]{false, true}) {
            try (Socket s = new Socket(InetAddress.getLoopbackAddress(), port)) {
                s.setTcpNoDelay(nodelay);
                OutputStream out = s.getOutputStream();
                InputStream in = s.getInputStream();
                int rounds = 20;
                byte[] header = new byte[4], body = new byte[40], reply = new byte[44];
                long t0 = System.nanoTime();
                for (int i = 0; i < rounds; i++) {
                    out.write(header);                       // first small segment: sent at once
                    out.write(body);                         // second small segment: Nagle holds it until the first is ACKed
                    int got = 0;
                    while (got < reply.length) got += in.read(reply, got, reply.length - got);
                }
                double us = (System.nanoTime() - t0) / 1e3 / rounds;
                System.out.printf("TCP_NODELAY=%-5b : %10.0f us per request/reply%n", nodelay, us);
            }
        }
        System.out.println("(On Linux the first line is typically ~40,000 us: Nagle waits for an ACK, the peer delays its ACK. macOS loopback does not reproduce it.)");

        System.out.println("\n== 1b. 200,000 one-byte write() calls: what Nagle is FOR (coalescing small writes) ==");
        try (ServerSocket sink = new ServerSocket(0, 50, InetAddress.getLoopbackAddress())) {
            for (int rep = 0; rep < 2; rep++) {
                for (boolean nodelay : new boolean[]{false, true}) {
                    Thread reader = new Thread(() -> {
                        try (Socket c = sink.accept()) { byte[] b = new byte[65536]; while (c.getInputStream().read(b) > 0) { } }
                        catch (IOException e) { /* demo */ }
                    });
                    reader.start();
                    try (Socket s = new Socket(InetAddress.getLoopbackAddress(), sink.getLocalPort())) {
                        s.setTcpNoDelay(nodelay);
                        OutputStream o = s.getOutputStream();
                        long t0 = System.nanoTime();
                        for (int i = 0; i < 200_000; i++) o.write(1);
                        o.flush();
                        if (rep == 1) System.out.printf("TCP_NODELAY=%-5b : %6.0f ms%n", nodelay, (System.nanoTime() - t0) / 1e6);
                    }
                    reader.join();
                }
            }
        }
    }

    // ---------- 2. 500 connections x 200 request/reply each: selector vs virtual threads -------------------
    static void concurrentClients() throws Exception {
        System.out.println("\n== 2. 100 concurrent connections, 500 ping-pongs each (client side = 100 virtual threads) ==");
        int selPort = startSelectorEcho(), vtPort = startVirtualThreadEcho();
        for (int rep = 0; rep < 3; rep++) {
            double a = hammer(selPort, 100, 500), b = hammer(vtPort, 100, 500);
            System.out.printf("run %d: selector server %6.0f ms | virtual-thread server %6.0f ms%n", rep, a, b);
        }
    }

    static double hammer(int port, int conns, int rounds) throws Exception {
        CountDownLatch done = new CountDownLatch(conns);
        long t0 = System.nanoTime();
        try (ExecutorService pool = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int c = 0; c < conns; c++) {
                pool.submit(() -> {
                    try (Socket s = new Socket(InetAddress.getLoopbackAddress(), port)) {
                        s.setTcpNoDelay(true);
                        OutputStream out = s.getOutputStream();
                        InputStream in = s.getInputStream();
                        byte[] msg = new byte[32], rep = new byte[32];
                        for (int i = 0; i < rounds; i++) {
                            out.write(msg);
                            int got = 0;
                            while (got < 32) got += in.read(rep, got, 32 - got);
                        }
                    } catch (IOException e) { System.out.println("client error: " + e); }
                    done.countDown();
                    return null;
                });
            }
            done.await();
        }
        return (System.nanoTime() - t0) / 1e6;
    }

    // ---------- 3. UDP multicast with sequence numbers and gap detection --------------------------------
    static void multicast() throws Exception {
        System.out.println("\n== 3. UDP multicast on loopback: 1 sender, 2 receivers, sequence numbers, 1 packet in 500 'lost' ==");
        InetAddress group = InetAddress.getByName("239.255.42.99");     // 239.0.0.0/8 = administratively scoped (private) multicast
        NetworkInterface ni = loopbackInterface();
        if (ni == null) { System.out.println("no multicast-capable loopback interface found; skipping"); return; }
        int port = 45678;
        int total = 10_000;
        List<DatagramChannel> rx = new ArrayList<>();
        for (int i = 0; i < 2; i++) {
            DatagramChannel ch = DatagramChannel.open(StandardProtocolFamily.INET);
            ch.setOption(StandardSocketOptions.SO_REUSEADDR, true);     // several receivers may share the port
            ch.bind(new InetSocketAddress(port));
            ch.join(group, ni);                                         // IGMP join: tells the network "send me this group"
            ch.configureBlocking(false);
            rx.add(ch);
        }
        DatagramChannel tx = DatagramChannel.open(StandardProtocolFamily.INET);
        tx.setOption(StandardSocketOptions.IP_MULTICAST_IF, ni);
        tx.setOption(StandardSocketOptions.IP_MULTICAST_LOOP, true);
        tx.setOption(StandardSocketOptions.IP_MULTICAST_TTL, 1);        // stay on the local network segment
        InetSocketAddress dest = new InetSocketAddress(group, port);

        ByteBuffer out = ByteBuffer.allocate(16);
        ByteBuffer in = ByteBuffer.allocate(16);
        long[] received = new long[2], gaps = new long[2], expect = new long[2];
        for (long seq = 0; seq <= total; seq++) {
            if (seq < total && seq % 500 != 499) {                      // every 500th packet is "lost": never sent
                out.clear(); out.putLong(seq).flip();
                tx.send(out, dest);
            }
            if (seq == total) Thread.sleep(100);                        // let the last packets arrive before the final drain
            for (int r = 0; r < 2; r++) {                               // drain whatever has arrived (non-blocking)
                DatagramChannel ch = rx.get(r);
                while (true) {
                    in.clear();
                    if (ch.receive(in) == null) break;
                    in.flip();
                    long got = in.getLong();
                    if (got != expect[r]) gaps[r] += got - expect[r];   // gap detection: this is what real feed handlers do
                    expect[r] = got + 1;
                    received[r]++;
                }
            }
        }
        for (int r = 0; r < 2; r++)
            System.out.printf("receiver %d: got %d packets, detected %d missing sequence numbers (20 were dropped; the last one, seq 9999, is invisible: no later packet reveals the gap)%n", r, received[r], gaps[r]);
        for (DatagramChannel c : rx) c.close();
        tx.close();
    }

    static NetworkInterface loopbackInterface() throws IOException {
        Enumeration<NetworkInterface> e = NetworkInterface.getNetworkInterfaces();
        while (e.hasMoreElements()) {
            NetworkInterface ni = e.nextElement();
            if (ni.isLoopback() && ni.isUp() && ni.supportsMulticast()) return ni;
        }
        return null;
    }
}
