import static org.junit.jupiter.api.Assertions.*;

import java.nio.ByteBuffer;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 1：ByteRing + FrameCodec + FrameDecoder（纯内存，无网络）。 */
class FramingTest {
    static ByteBuffer bb(int... bytes) {
        ByteBuffer b = ByteBuffer.allocate(bytes.length);
        for (int x : bytes) b.put((byte) x);
        b.flip();
        return b;
    }

    // ------------------------------------------------------------ ByteRing

    @Test @Tag("part1")
    void ringBasicWriteRead() {
        ByteRing r = new ByteRing(8);
        assertEquals(8, r.capacity()); assertEquals(0, r.size()); assertEquals(8, r.free()); assertTrue(r.isEmpty());
        assertEquals(3, r.write(bb(1, 2, 3)));
        assertEquals(3, r.size());
        ByteBuffer dst = ByteBuffer.allocate(10);
        assertEquals(3, r.read(dst));
        assertEquals(3, dst.position());
        assertArrayEquals(new byte[]{1, 2, 3}, java.util.Arrays.copyOf(dst.array(), 3));
        assertTrue(r.isEmpty());
        assertEquals(0, r.read(ByteBuffer.allocate(4)));
    }

    @Test @Tag("part1") @Tag("edge")
    void ringWrapsAroundAndSplitsCopy() {
        ByteRing r = new ByteRing(8);
        r.write(bb(1, 2, 3, 4, 5, 6));
        assertArrayEquals(new byte[]{1, 2, 3, 4}, r.take(4));
        assertEquals(5, r.write(bb(7, 8, 9, 10, 11)));          // 尾部只剩 2 格 + 头部 4 格，需要分两段拷贝
        assertEquals(7, r.size());
        assertArrayEquals(new byte[]{5, 6, 7, 8, 9, 10, 11}, r.take(7));
    }

    @Test @Tag("part1") @Tag("edge")
    void ringPartialWriteWhenFull() {
        ByteRing r = new ByteRing(4);
        ByteBuffer src = bb(1, 2, 3, 4, 5, 6);
        assertEquals(4, r.write(src));
        assertEquals(4, src.position());                          // 只前进 4
        assertEquals(2, src.remaining());
        assertEquals(0, r.write(src));                            // 满了：一个字节也写不进
        assertEquals(0, r.free());
    }

    @Test @Tag("part1") @Tag("edge")
    void ringPartialReadIntoSmallBuffer() {
        ByteRing r = new ByteRing(8);
        r.write(bb(1, 2, 3, 4, 5));
        ByteBuffer dst = ByteBuffer.allocate(2);
        assertEquals(2, r.read(dst));
        assertEquals(3, r.size());
        assertArrayEquals(new byte[]{3, 4, 5}, r.take(3));
    }

    @Test @Tag("part1")
    void ringWriteAllIsAtomic() {
        ByteRing r = new ByteRing(5);
        assertTrue(r.writeAll(new byte[]{9, 9, 1, 2, 3, 9}, 2, 3));   // off/len
        assertFalse(r.writeAll(new byte[]{4, 5, 6}, 0, 3));            // 只剩 2 格：全不写
        assertEquals(3, r.size());
        assertTrue(r.writeAll(new byte[]{4, 5}, 0, 2));
        assertArrayEquals(new byte[]{1, 2, 3, 4, 5}, r.take(5));
        assertThrows(IndexOutOfBoundsException.class, () -> r.writeAll(new byte[2], 1, 5));
    }

    @Test @Tag("part1") @Tag("edge")
    void ringPeekIntIsBigEndianAcrossWrapAndDoesNotConsume() {
        ByteRing r = new ByteRing(6);
        r.write(bb(0, 0, 0, 0));
        r.skip(4);
        r.write(bb(0x12, 0x34, 0x56, 0x78, 0x9A));                 // 头在位置 4，数据跨过末尾
        assertEquals(0x12345678, r.peekInt());
        assertEquals(0x3456789A, r.peekInt(1));
        assertEquals(5, r.size());
        assertThrows(IllegalStateException.class, () -> r.peekInt(2));
        ByteRing neg = new ByteRing(4);
        neg.write(bb(0xFF, 0xFF, 0xFF, 0xFF));
        assertEquals(-1, neg.peekInt());                           // 符号位
    }

    @Test @Tag("part1") @Tag("edge")
    void ringTakeSkipErrorsLeaveStateUntouched() {
        ByteRing r = new ByteRing(4);
        r.write(bb(1, 2));
        assertThrows(IllegalStateException.class, () -> r.take(3));
        assertThrows(IllegalStateException.class, () -> r.skip(3));
        assertThrows(IllegalArgumentException.class, () -> r.take(-1));
        assertEquals(2, r.size());
        r.skip(2);
        assertTrue(r.isEmpty());
        assertArrayEquals(new byte[0], r.take(0));
        r.write(bb(7)); r.clear();
        assertTrue(r.isEmpty());
        assertThrows(IllegalArgumentException.class, () -> new ByteRing(0));
    }

    @Test @Tag("part1") @Tag("edge")
    void ringMatchesDequeModelOnRandomOps() {
        Random rnd = new Random(3);
        for (int cap : new int[]{1, 2, 7, 16, 100}) {
            ByteRing r = new ByteRing(cap);
            ArrayDeque<Byte> model = new ArrayDeque<>();
            for (int i = 0; i < 3000; i++) {
                if (rnd.nextBoolean()) {
                    byte[] data = new byte[rnd.nextInt(cap + 3)];
                    rnd.nextBytes(data);
                    ByteBuffer src = ByteBuffer.wrap(data);
                    int n = r.write(src);
                    assertEquals(Math.min(data.length, cap - model.size()), n);
                    for (int k = 0; k < n; k++) model.addLast(data[k]);
                } else {
                    ByteBuffer dst = ByteBuffer.allocate(rnd.nextInt(cap + 3));
                    int n = r.read(dst);
                    assertEquals(Math.min(dst.capacity(), model.size()), n);
                    for (int k = 0; k < n; k++) assertEquals(model.pollFirst(), dst.get(k));
                }
                assertEquals(model.size(), r.size());
            }
        }
    }

    // ------------------------------------------------------------ FrameCodec

    @Test @Tag("part1")
    void encodeWritesBigEndianLengthThenPayload() {
        ByteRing r = new ByteRing(32);
        assertTrue(FrameCodec.encode(r, new byte[]{10, 20, 30}, 100));
        assertArrayEquals(new byte[]{0, 0, 0, 3, 10, 20, 30}, r.take(7));
        byte[] big = new byte[300];
        assertTrue(FrameCodec.encode(new ByteRing(400), big, 300));
        ByteRing r2 = new ByteRing(400);
        FrameCodec.encode(r2, big, 300);
        assertArrayEquals(new byte[]{0, 0, 1, 44}, r2.take(4));     // 300 = 0x012C
    }

    @Test @Tag("part1") @Tag("edge")
    void encodeEmptyPayloadIsLegal() {
        ByteRing r = new ByteRing(8);
        assertTrue(FrameCodec.encode(r, new byte[0], 10));
        assertArrayEquals(new byte[]{0, 0, 0, 0}, r.take(4));
    }

    @Test @Tag("part1") @Tag("edge")
    void encodeReturnsFalseWithoutPartialWriteWhenFull() {
        ByteRing r = new ByteRing(10);
        assertTrue(FrameCodec.encode(r, new byte[3], 10));          // 7 字节
        assertFalse(FrameCodec.encode(r, new byte[2], 10));         // 需要 6，只剩 3
        assertEquals(7, r.size());                                  // 没有写进半个头
        assertFalse(FrameCodec.encode(r, new byte[]{}, 10));   // 需要 4，只剩 3
        r.skip(7);
        assertTrue(FrameCodec.encode(r, new byte[6], 10));          // 恰好 10
        assertEquals(0, r.free());
    }

    @Test @Tag("part1") @Tag("edge")
    void encodeRejectsOversizedPayload() {
        ByteRing r = new ByteRing(64);
        assertThrows(IllegalArgumentException.class, () -> FrameCodec.encode(r, new byte[11], 10));
        assertTrue(FrameCodec.encode(r, new byte[10], 10));         // 恰好 maxFrame
        assertThrows(NullPointerException.class, () -> FrameCodec.encode(r, null, 10));
    }

    // ------------------------------------------------------------ FrameDecoder

    static byte[] encodeAll(int maxFrame, List<byte[]> msgs) {
        int total = msgs.stream().mapToInt(m -> 4 + m.length).sum();
        ByteRing r = new ByteRing(Math.max(1, total));
        for (byte[] m : msgs) assertTrue(FrameCodec.encode(r, m, maxFrame));
        return r.take(total);
    }

    @Test @Tag("part1")
    void decoderReturnsWholeFramesAndNullWhenIncomplete() {
        FrameDecoder d = new FrameDecoder(100, 256);
        assertNull(d.next());
        byte[] stream = encodeAll(100, List.of(new byte[]{1, 2}, new byte[]{3}, new byte[0]));
        assertEquals(stream.length, d.feed(ByteBuffer.wrap(stream)));
        assertArrayEquals(new byte[]{1, 2}, d.next());
        assertArrayEquals(new byte[]{3}, d.next());
        assertArrayEquals(new byte[0], d.next());
        assertNull(d.next());
        assertEquals(0, d.buffered());
    }

    @Test @Tag("part1") @Tag("edge")
    void decoderHandlesEverySplitPointOfAStream() {
        List<byte[]> msgs = List.of("hello".getBytes(), new byte[0], "w".getBytes(), new byte[20]);
        byte[] stream = encodeAll(50, msgs);
        for (int cut = 0; cut <= stream.length; cut++) {
            FrameDecoder d = new FrameDecoder(50, 128);
            List<byte[]> got = new ArrayList<>();
            d.feed(ByteBuffer.wrap(stream, 0, cut));
            for (byte[] m; (m = d.next()) != null; ) got.add(m);
            d.feed(ByteBuffer.wrap(stream, cut, stream.length - cut));
            for (byte[] m; (m = d.next()) != null; ) got.add(m);
            assertEquals(msgs.size(), got.size(), "cut=" + cut);
            for (int i = 0; i < msgs.size(); i++) assertArrayEquals(msgs.get(i), got.get(i), "cut=" + cut + " i=" + i);
        }
    }

    @Test @Tag("part1") @Tag("edge")
    void decoderByteAtATime() {
        List<byte[]> msgs = List.of("abc".getBytes(), "defgh".getBytes());
        byte[] stream = encodeAll(10, msgs);
        FrameDecoder d = new FrameDecoder(10, 14);
        List<byte[]> got = new ArrayList<>();
        for (byte b : stream) {
            assertEquals(1, d.feed(ByteBuffer.wrap(new byte[]{b})));
            byte[] m = d.next();
            if (m != null) got.add(m);
        }
        assertEquals(2, got.size());
        assertArrayEquals("abc".getBytes(), got.get(0));
        assertArrayEquals("defgh".getBytes(), got.get(1));
    }

    @Test @Tag("part1") @Tag("edge")
    void decoderAcceptsFrameOfExactlyMaxFrame() {
        FrameDecoder d = new FrameDecoder(5, 9);                    // 容量恰好 maxFrame + 4
        byte[] stream = encodeAll(5, List.of(new byte[]{1, 2, 3, 4, 5}));
        assertEquals(9, d.feed(ByteBuffer.wrap(stream)));
        assertArrayEquals(new byte[]{1, 2, 3, 4, 5}, d.next());
        assertThrows(IllegalArgumentException.class, () -> new FrameDecoder(5, 8));
    }

    @Test @Tag("part1") @Tag("edge")
    void decoderFeedIsBoundedAndResumesAfterDrain() {
        FrameDecoder d = new FrameDecoder(4, 12);
        byte[] stream = encodeAll(4, List.of(new byte[]{1}, new byte[]{2, 2}, new byte[]{3, 3, 3}, new byte[]{4}));
        ByteBuffer src = ByteBuffer.wrap(stream);
        int fed = d.feed(src);
        assertEquals(12, fed);                                     // 只吃得下 12 字节
        assertEquals(stream.length - 12, src.remaining());
        assertEquals(0, d.free());
        List<byte[]> got = new ArrayList<>();
        for (int guard = 0; guard < 20 && got.size() < 4; guard++) {
            for (byte[] m; (m = d.next()) != null; ) got.add(m);
            d.feed(src);
        }
        assertEquals(4, got.size());
        assertArrayEquals(new byte[]{3, 3, 3}, got.get(2));
        assertEquals(0, src.remaining());
    }

    @Test @Tag("part1") @Tag("edge")
    void decoderRejectsNegativeAndOversizedLengthsAndStaysFailed() {
        FrameDecoder neg = new FrameDecoder(10, 64);
        neg.feed(bb(0xFF, 0xFF, 0xFF, 0xFF, 1, 2, 3));
        assertThrows(FrameException.class, neg::next);
        assertThrows(FrameException.class, neg::next);              // 粘性
        assertTrue(neg.hasFrame());

        FrameDecoder big = new FrameDecoder(10, 64);
        big.feed(bb(0, 0, 0, 11));                                  // maxFrame + 1：只看到头就必须报错，不能等 11 字节
        assertThrows(FrameException.class, big::next);

        FrameDecoder huge = new FrameDecoder(10, 64);
        huge.feed(bb(0x7F, 0xFF, 0xFF, 0xFF));                      // 2^31 - 1：不能尝试分配
        assertThrows(FrameException.class, huge::next);
    }

    @Test @Tag("part1")
    void decoderHasFrameAndTruncatedTail() {
        FrameDecoder d = new FrameDecoder(10, 64);
        assertFalse(d.hasFrame()); assertFalse(d.hasTruncatedTail());
        d.feed(bb(0, 0));                                           // 半个头
        assertFalse(d.hasFrame()); assertTrue(d.hasTruncatedTail());
        d.feed(bb(0, 2, 7));                                        // 头完整，负载 1/2
        assertFalse(d.hasFrame()); assertTrue(d.hasTruncatedTail());
        d.feed(bb(8, 0, 0, 0, 0));                                  // 补齐第一帧 + 一个空帧
        assertTrue(d.hasFrame()); assertFalse(d.hasTruncatedTail());
        d.feed(bb(0, 0));                                           // 完整帧后面又来半个头
        assertTrue(d.hasTruncatedTail());
        assertArrayEquals(new byte[]{7, 8}, d.next());
        assertTrue(d.hasTruncatedTail());                           // 空帧还在，后面还有半个头
        assertArrayEquals(new byte[0], d.next());
        assertTrue(d.hasTruncatedTail());
        assertNull(d.next());
    }

    @Test @Tag("part1") @Tag("edge")
    void decoderRandomChunkingRoundTrip() {
        Random rnd = new Random(5);
        for (int round = 0; round < 40; round++) {
            int maxFrame = 1 + rnd.nextInt(60);
            List<byte[]> msgs = new ArrayList<>();
            for (int i = 0; i < 100; i++) { byte[] m = new byte[rnd.nextInt(maxFrame + 1)]; rnd.nextBytes(m); msgs.add(m); }
            byte[] stream = encodeAll(maxFrame, msgs);
            FrameDecoder d = new FrameDecoder(maxFrame, maxFrame + 4 + rnd.nextInt(40));
            ByteBuffer src = ByteBuffer.wrap(stream);
            List<byte[]> got = new ArrayList<>();
            for (int guard = 0; got.size() < msgs.size(); guard++) {
                assertTrue(guard < 100_000, "decoder stuck");
                int chunk = 1 + rnd.nextInt(30);
                ByteBuffer slice = src.slice(src.position(), Math.min(chunk, src.remaining()));
                int used = d.feed(slice);
                src.position(src.position() + used);
                for (byte[] m; (m = d.next()) != null; ) got.add(m);
            }
            for (int i = 0; i < msgs.size(); i++) assertArrayEquals(msgs.get(i), got.get(i));
        }
    }

    @Test @Tag("part1") @Tag("perf")
    void millionMessagesThroughRingAndDecoderFast() {
        org.junit.jupiter.api.Assertions.assertTimeoutPreemptively(java.time.Duration.ofSeconds(2), () -> {
            ByteRing ring = new ByteRing(1 << 16);
            FrameDecoder d = new FrameDecoder(64, 1 << 12);
            byte[] msg = new byte[32];
            ByteBuffer chunk = ByteBuffer.allocate(1 << 12);
            long got = 0;
            for (int i = 0; i < 1_000_000; i++) {
                msg[0] = (byte) i;
                if (!FrameCodec.encode(ring, msg, 64)) fail("ring unexpectedly full");
                if ((i & 63) == 63) {                                    // 每 64 条搬一次，模拟 socket 一次读到一批
                    chunk.clear();
                    ring.read(chunk);
                    chunk.flip();
                    while (chunk.hasRemaining()) {
                        d.feed(chunk);
                        for (byte[] m; (m = d.next()) != null; ) got++;
                    }
                }
            }
            assertEquals(1_000_000 - (1_000_000 % 64), got);
        });
    }
}
