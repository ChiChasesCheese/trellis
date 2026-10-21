import java.util.ArrayDeque;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.SequencedMap;
import java.util.TreeMap;

/**
 * J09 例 3（贴近真实）：简化的订单簿。
 * - 买盘/卖盘：按价格排序的 TreeMap，当成 SequencedMap 用 -> firstEntry() 就是最优价；
 * - 每个价位：LinkedHashMap<id, qty>，按到达顺序排队 -> firstEntry() 是队头；加量 == putLast 重新排队；
 * - 最近成交：ArrayDeque，reversed() 从新到旧遍历。
 */
public class J09Ex3 {

    static final class Level {
        final SequencedMap<Long, Long> fifo = new LinkedHashMap<>();   // id -> 剩余数量
        long total;
    }

    // 买盘：价格从高到低，最优买价 = 第一个；卖盘：从低到高，最优卖价 = 第一个
    final SequencedMap<Long, Level> bids = new TreeMap<>(Comparator.reverseOrder());
    final SequencedMap<Long, Level> asks = new TreeMap<>();
    final ArrayDeque<String> tape = new ArrayDeque<>();

    void rest(SequencedMap<Long, Level> book, long id, long px, long qty) {
        Level lv = book.computeIfAbsent(px, k -> new Level());
        lv.fifo.put(id, qty);
        lv.total += qty;
    }

    /** 加量 == 重新排队（时间优先被重置）。putLast 对已存在的 key 把它挪到末尾。 */
    void increase(SequencedMap<Long, Level> book, long px, long id, long extra) {
        Level lv = book.get(px);
        long newQty = lv.fifo.get(id) + extra;
        lv.fifo.putLast(id, newQty);
        lv.total += extra;
    }

    /** 买单 (px, qty) 去吃卖盘：最优价永远是 asks.firstEntry()。 */
    long buy(long takerId, long limit, long qty) {
        long left = qty;
        while (left > 0) {
            var top = asks.firstEntry();                         // 最优卖价；空簿返回 null
            if (top == null || top.getKey() > limit) break;
            Level lv = top.getValue();
            var head = lv.fifo.firstEntry();                     // 该价位排在最前的订单
            long fill = Math.min(left, head.getValue());
            tape.addLast("TRADE taker=" + takerId + " maker=" + head.getKey() + " px=" + top.getKey() + " qty=" + fill);
            left -= fill;
            lv.total -= fill;
            if (fill == head.getValue()) {
                lv.fifo.pollFirstEntry();                        // 队头成交完，出队
                if (lv.fifo.isEmpty()) asks.pollFirstEntry();    // 这个价位空了，整档删掉
            } else {
                lv.fifo.put(head.getKey(), head.getValue() - fill);        // 部分成交：已存在的 key，put 只改数量、位置不变，仍在队头
            }
        }
        return left;
    }

    public static void main(String[] args) {
        var ob = new J09Ex3();
        ob.rest(ob.asks, 1, 101, 5);
        ob.rest(ob.asks, 2, 101, 3);
        ob.rest(ob.asks, 3, 102, 4);
        ob.rest(ob.bids, 10, 99, 7);
        ob.rest(ob.bids, 11, 100, 2);

        System.out.println("best bid=" + ob.bids.firstEntry().getKey() + " best ask=" + ob.asks.firstEntry().getKey());

        long left = ob.buy(4, 101, 6);                           // 吃掉 id=1 的 5 手，id=2 的 1 手
        System.out.println("left=" + left + " best ask=" + ob.asks.firstEntry().getKey()
                + " queue@101=" + ob.asks.firstEntry().getValue().fifo);

        ob.increase(ob.asks, 101, 2, 4);                         // id=2 加量 -> 重新排到队尾（队里只有它一个）
        ob.rest(ob.asks, 5, 101, 9);                             // id=5 排在 id=2 后面
        ob.increase(ob.asks, 101, 2, 1);                         // id=2 再加量 -> 排到 id=5 后面
        System.out.println("queue@101=" + ob.asks.firstEntry().getValue().fifo);

        left = ob.buy(6, 102, 10);
        System.out.println("left=" + left);

        System.out.println("最近成交（新 -> 旧）：");
        for (String line : ob.tape.reversed()) System.out.println("  " + line);
        System.out.println(List.copyOf(ob.bids.sequencedKeySet()));    // 买盘价位：高 -> 低
    }
}
