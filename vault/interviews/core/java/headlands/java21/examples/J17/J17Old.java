import java.nio.ByteBuffer;
import java.nio.ByteOrder;

/** J17 旧写法：ByteBuffer.allocateDirect。三个痛点：int 下标(最多 2GB)、释放时间不可控(靠 GC/Cleaner)、没有"结构体布局"。 */
public class J17Old {
    public static void main(String[] args) {
        // 一条记录 = id(8) + price(8) + qty(4) + 4 字节填充 = 24 字节。所有偏移量都得自己手算
        final int REC = 24, ID = 0, PX = 8, QTY = 16;
        int n = 1_000;
        ByteBuffer buf = ByteBuffer.allocateDirect(n * REC).order(ByteOrder.nativeOrder());
        for (int i = 0; i < n; i++) {
            buf.putLong(i * REC + ID, i);
            buf.putLong(i * REC + PX, 18_950 + i);
            buf.putInt(i * REC + QTY, 100);
        }
        long sum = 0;
        for (int i = 0; i < n; i++) sum += buf.getLong(i * REC + PX) * buf.getInt(i * REC + QTY);
        System.out.println("notional = " + sum);

        // 痛点 1：容量是 int -> 最大 2^31-1 字节；想要 4GB 的表？不行，只能拆成多个 buffer
        // 痛点 2：没有 close()。这块堆外内存什么时候还给操作系统？等 GC 发现 buf 对象不可达之后，由 Cleaner 释放。
        //        GC 不紧张时可能很久不释放；-XX:MaxDirectMemorySize 满了就 OutOfMemoryError: Direct buffer memory
        // 痛点 3：偏移量(24, 8, 16)是魔法数字，改了结构要全部改；类型靠人记
        long want = 3_000_000_000L;                       // 想要 3GB 的表
        try {
            ByteBuffer.allocateDirect((int) want);          // 容量参数是 int：3e9 强转后变成负数
        } catch (IllegalArgumentException e) {
            System.out.println("想要 " + want + " 字节 -> (int) = " + (int) want + " -> " + e.getClass().getSimpleName());
        }
    }
}
