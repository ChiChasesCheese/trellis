import java.io.IOException;
import java.lang.foreign.Arena;
import java.lang.foreign.FunctionDescriptor;
import java.lang.foreign.Linker;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.ValueLayout;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.VarHandle;
import java.nio.ByteOrder;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.locks.LockSupport;

/**
 * Companion to os_processes_threads_ipc.md.
 *   (no args)                       : syscall cost, thread hand-off latency, mmap persistence, SPSC ring in one JVM
 *   producer|consumer <file> <n>    : the same SPSC ring shared by TWO separate JVM processes through a mapped file
 * Needs preview APIs (java.lang.foreign is a preview API in JDK 21):
 *   javac --release 21 --enable-preview IpcDemo.java
 *   java --enable-preview --enable-native-access=ALL-UNNAMED IpcDemo
 */
public class IpcDemo {
    static volatile long sink;

    // ------------------------------------------------------------------------------------------
    // SPSC (single-producer single-consumer) ring buffer of longs living in a MemorySegment.
    // Layout (bytes):  [0,128)   head   (next slot the consumer will read)   -- own cache line(s)
    //                  [128,256) tail   (next slot the producer will write)  -- own cache line(s)
    //                  [256, ..) slots  (capacity * 8 bytes, capacity is a power of two)
    // Only the producer writes `tail` and slots; only the consumer writes `head`. No locks, no CAS.
    // ------------------------------------------------------------------------------------------
    static final class SpscRing {
        static final VarHandle LONG = ValueLayout.JAVA_LONG.varHandle();   // coordinates in JDK 21: (MemorySegment)
        static final int HEADER = 256;
        final MemorySegment headSeg, tailSeg, slots;
        final int capacity, mask;
        long cachedHead, cachedTail;                                       // local copies of the other side's index

        SpscRing(MemorySegment mem, int capacity) {
            if (Integer.bitCount(capacity) != 1) throw new IllegalArgumentException("capacity must be a power of two");
            this.capacity = capacity;
            this.mask = capacity - 1;
            this.headSeg = mem.asSlice(0, 8);
            this.tailSeg = mem.asSlice(128, 8);
            this.slots = mem.asSlice(HEADER, (long) capacity * 8);
        }

        static long bytesFor(int capacity) { return HEADER + (long) capacity * 8; }

        /** Producer side. Returns false if the ring is full. */
        boolean offer(long v) {
            long tail = (long) LONG.get(tailSeg);                          // plain read: we are the only writer
            if (tail - cachedHead == capacity) {                           // looks full: refresh the consumer's index
                cachedHead = (long) LONG.getAcquire(headSeg);
                if (tail - cachedHead == capacity) return false;
            }
            slots.set(ValueLayout.JAVA_LONG, (tail & mask) * 8, v);        // 1) write the payload ...
            LONG.setRelease(tailSeg, tail + 1);                            // 2) ... then publish it (release)
            return true;
        }

        /** Consumer side. Returns Long.MIN_VALUE if the ring is empty. */
        long poll() {
            long head = (long) LONG.get(headSeg);
            if (head == cachedTail) {                                      // looks empty: refresh the producer's index
                cachedTail = (long) LONG.getAcquire(tailSeg);              // acquire pairs with the producer's release
                if (head == cachedTail) return Long.MIN_VALUE;
            }
            long v = (long) slots.get(ValueLayout.JAVA_LONG, (head & mask) * 8);
            LONG.setRelease(headSeg, head + 1);                            // free the slot for the producer
            return v;
        }
    }

    public static void main(String[] args) throws Throwable {
        if (args.length == 3) { crossProcess(args[0], Path.of(args[1]), Integer.parseInt(args[2])); return; }
        syscallCost();
        handoffLatency();
        mmapPersistence();
        ringInOneJvm();
    }

    // 1. A real system call through the FFM API: write(fd, buf, 1) to /dev/null ----------------------------
    static void syscallCost() throws Throwable {
        System.out.println("== 1. cost of a trivial system call (write 1 byte to /dev/null via FFM downcall) ==");
        Linker linker = Linker.nativeLinker();
        var lookup = linker.defaultLookup();
        MethodHandle open = linker.downcallHandle(lookup.find("open").orElseThrow(),
                FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.ADDRESS, ValueLayout.JAVA_INT));
        MethodHandle write = linker.downcallHandle(lookup.find("write").orElseThrow(),
                FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.JAVA_INT, ValueLayout.ADDRESS, ValueLayout.JAVA_LONG));
        MethodHandle abs = linker.downcallHandle(lookup.find("abs").orElseThrow(),
                FunctionDescriptor.of(ValueLayout.JAVA_INT, ValueLayout.JAVA_INT));   // libc call that does NOT enter the kernel
        try (Arena arena = Arena.ofConfined()) {
            int fd = (int) open.invokeExact(arena.allocateUtf8String("/dev/null"), 1 /* O_WRONLY */);
            MemorySegment buf = arena.allocate(8);
            int n = 5_000_000;
            long acc = 0;
            for (int i = 0; i < 1_000_000; i++) { acc += (long) write.invokeExact(fd, buf, 1L); acc += (int) abs.invokeExact(-i); }  // warm-up
            long t0 = System.nanoTime();
            for (int i = 0; i < n; i++) acc += (long) write.invokeExact(fd, buf, 1L);
            long t1 = System.nanoTime();
            for (int i = 0; i < n; i++) acc += (int) abs.invokeExact(-i);
            long t2 = System.nanoTime();
            sink = acc;
            System.out.printf("write(fd,buf,1): %.0f ns per call   |   abs() (no kernel entry, same FFM overhead): %.1f ns%n",
                    (t1 - t0) / (double) n, (t2 - t1) / (double) n);
        }
    }

    // 2. Hand-off between two threads: park/unpark vs spinning ------------------------------------------
    static void handoffLatency() throws Exception {
        System.out.println("\n== 2. ping-pong between two threads: round-trip time ==");
        int rounds = 200_000;
        // (a) blocking hand-off: the sleeping thread must be woken by the kernel scheduler
        final Thread[] th = new Thread[2];
        final java.util.concurrent.atomic.AtomicInteger flag = new java.util.concurrent.atomic.AtomicInteger(0);
        th[1] = new Thread(() -> {
            for (int i = 0; i < rounds; i++) {
                while (flag.get() != 1) LockSupport.park();
                flag.set(0);
                LockSupport.unpark(th[0]);
            }
        });
        th[0] = Thread.currentThread();
        th[1].start();
        long t0 = System.nanoTime();
        for (int i = 0; i < rounds; i++) {
            flag.set(1);
            LockSupport.unpark(th[1]);
            while (flag.get() != 0) LockSupport.park();
        }
        double parkNs = (System.nanoTime() - t0) / (double) rounds;
        th[1].join();

        // (b) busy-spin hand-off: both threads keep a core hot and just watch a variable
        final java.util.concurrent.atomic.AtomicInteger f2 = new java.util.concurrent.atomic.AtomicInteger(0);
        Thread ponger = new Thread(() -> {
            for (int i = 0; i < rounds; i++) {
                while (f2.get() != 1) Thread.onSpinWait();
                f2.set(0);
            }
        });
        ponger.start();
        long t2 = System.nanoTime();
        for (int i = 0; i < rounds; i++) {
            f2.set(1);
            while (f2.get() != 0) Thread.onSpinWait();
        }
        double spinNs = (System.nanoTime() - t2) / (double) rounds;
        ponger.join();
        System.out.printf("park/unpark round trip: %8.0f ns%n", parkNs);
        System.out.printf("busy-spin round trip  : %8.0f ns%n", spinNs);
    }

    // 3. Memory-mapped file: write through the mapping, read it back through a normal read ------------------
    static void mmapPersistence() throws IOException {
        System.out.println("\n== 3. memory-mapped file ==");
        Path p = Files.createTempFile("mmap-demo", ".bin");
        try (FileChannel ch = FileChannel.open(p, StandardOpenOption.READ, StandardOpenOption.WRITE)) {
            // classic API (stable, 2 GB limit per mapping, unmapped only when the GC collects it)
            MappedByteBuffer mb = ch.map(FileChannel.MapMode.READ_WRITE, 0, 4096);
            mb.order(ByteOrder.nativeOrder());                             // default is BIG-endian; FFM's JAVA_LONG is native-endian!
            mb.putLong(0, 0xCAFEBABEL);
            mb.force();                                                    // msync: ask the OS to flush to the device
            // FFM API (JDK 21 preview): 64-bit sizes, deterministic unmap when the Arena closes
            try (Arena arena = Arena.ofConfined()) {
                MemorySegment seg = ch.map(FileChannel.MapMode.READ_WRITE, 0, 4096, arena);
                System.out.printf("read through FFM mapping: 0x%X, segment size %d%n", seg.get(ValueLayout.JAVA_LONG, 0), seg.byteSize());
                seg.set(ValueLayout.JAVA_LONG, 8, 42L);
            }                                                              // memory is unmapped here
            java.nio.ByteBuffer plain = java.nio.ByteBuffer.allocate(16).order(ByteOrder.nativeOrder());
            ch.read(plain, 0);
            plain.flip();
            System.out.printf("read through read(2) path: 0x%X and %d%n", plain.getLong(), plain.getLong());
        } finally {
            Files.deleteIfExists(p);
        }
    }

    // 4. The ring inside one JVM (two threads) vs ArrayBlockingQueue ----------------------------------------
    static void ringInOneJvm() throws Exception {
        System.out.println("\n== 4. SPSC ring over a mapped file vs ArrayBlockingQueue (two threads, 20M longs) ==");
        int n = 20_000_000, cap = 1 << 16;
        for (int rep = 0; rep < 5; rep++) {
            Path p = Files.createTempFile("ring", ".bin");
            try (FileChannel ch = FileChannel.open(p, StandardOpenOption.READ, StandardOpenOption.WRITE);
                 Arena arena = Arena.ofShared()) {
                MemorySegment mem = ch.map(FileChannel.MapMode.READ_WRITE, 0, SpscRing.bytesFor(cap), arena);
                SpscRing ring = new SpscRing(mem, cap);
                long t0 = System.nanoTime();
                Thread prod = new Thread(() -> { for (long i = 0; i < n; i++) while (!ring.offer(i)) Thread.onSpinWait(); });
                prod.start();
                long expected = 0;
                while (expected < n) {
                    long v = ring.poll();
                    if (v == Long.MIN_VALUE) { Thread.onSpinWait(); continue; }
                    if (v != expected) throw new IllegalStateException("out of order: " + v + " expected " + expected);
                    expected++;
                }
                prod.join();
                double sec = (System.nanoTime() - t0) / 1e9;
                System.out.printf("run %d: mmap SPSC ring     : %.2f s -> %.1f M msgs/s%n", rep, sec, n / sec / 1e6);
            } finally {
                Files.deleteIfExists(p);
            }
            BlockingQueue<Long> q = new ArrayBlockingQueue<>(cap);
            long t0 = System.nanoTime();
            Thread prod = new Thread(() -> { try { for (long i = 0; i < n; i++) q.put(i); } catch (InterruptedException e) { } });
            prod.start();
            for (long i = 0; i < n; i++) if (q.take() != i) throw new IllegalStateException();
            prod.join();
            double sec = (System.nanoTime() - t0) / 1e9;
            System.out.printf("run %d: ArrayBlockingQueue : %.2f s -> %.1f M msgs/s%n", rep, sec, n / sec / 1e6);
        }
    }

    // 5. Two processes sharing the ring through the same file -----------------------------------------------
    static void crossProcess(String role, Path file, int n) throws Exception {
        int cap = 1 << 16;
        try (FileChannel ch = FileChannel.open(file, StandardOpenOption.CREATE, StandardOpenOption.READ, StandardOpenOption.WRITE);
             Arena arena = Arena.ofShared()) {
            MemorySegment mem = ch.map(FileChannel.MapMode.READ_WRITE, 0, SpscRing.bytesFor(cap), arena);
            SpscRing ring = new SpscRing(mem, cap);
            long pid = ProcessHandle.current().pid();
            if (role.equals("producer")) {
                long t0 = System.nanoTime();
                for (long i = 0; i < n; i++) while (!ring.offer(i)) Thread.onSpinWait();
                System.out.printf("[pid %d] producer wrote %d msgs in %.2f s%n", pid, n, (System.nanoTime() - t0) / 1e9);
            } else {
                long t0 = 0, expected = 0;
                while (expected < n) {
                    long v = ring.poll();
                    if (v == Long.MIN_VALUE) { Thread.onSpinWait(); continue; }
                    if (expected == 0) t0 = System.nanoTime();          // start the clock at the first message, not at start-up
                    if (v != expected) throw new IllegalStateException("out of order: " + v + " expected " + expected);
                    expected++;
                }
                double sec = (System.nanoTime() - t0) / 1e9;
                System.out.printf("[pid %d] consumer read %d msgs in order, %.1f M msgs/s%n", pid, n, n / sec / 1e6);
            }
        }
    }
}
