import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/**
 * Part 2：仓位与盈亏，FIFO 配对。
 *
 * 每个标的维护一队「未平仓 lot」（qty, px），队内所有 lot 方向相同（dir = +1 多 / -1 空）。
 * 新成交与 dir 同向 → 追加 lot；反向 → 从队首开始平仓，每平一段实现 dir * (成交价 - lot价) * 数量；
 * 平完还有剩余 → 翻转：剩余部分作为反方向的新 lot。全程整数，无舍入。
 */
public final class PositionBook {
    private static final class Lot {
        long qty;
        final long px;

        Lot(long qty, long px) { this.qty = qty; this.px = px; }
    }

    private static final class Book {
        final ArrayDeque<Lot> lots = new ArrayDeque<>();
        int dir;                 // +1 多头, -1 空头, 0 平
        long realized;
    }

    private final Map<String, Book> books = new HashMap<>();

    public void onFill(String symbol, Side side, long qty, long px) {
        Objects.requireNonNull(symbol, "symbol");
        Objects.requireNonNull(side, "side");
        if (qty <= 0 || px <= 0) throw new IllegalArgumentException("qty and px must be > 0");
        Book b = books.computeIfAbsent(symbol, k -> new Book());
        int s = side.sign();
        if (b.dir == 0 || b.dir == s) {
            b.lots.addLast(new Lot(qty, px));
            b.dir = s;
            return;
        }
        long remaining = qty;
        long realized = b.realized;
        // 先只读地算出实现盈亏（溢出会在这里抛，此时还没改任何东西），再一次性提交
        long pnl = 0;
        for (Lot lot : b.lots) {
            if (remaining == 0) break;
            long c = Math.min(remaining, lot.qty);
            pnl = Math.addExact(pnl, Math.multiplyExact((long) b.dir * (px - lot.px), c));
            remaining -= c;
        }
        long newRealized = Math.addExact(realized, pnl);
        // 提交（以下不会再抛异常）
        remaining = qty;
        while (remaining > 0 && !b.lots.isEmpty()) {
            Lot lot = b.lots.peekFirst();
            long c = Math.min(remaining, lot.qty);
            lot.qty -= c;
            remaining -= c;
            if (lot.qty == 0) b.lots.pollFirst();
        }
        b.realized = newRealized;
        if (remaining > 0) {
            b.lots.addLast(new Lot(remaining, px));
            b.dir = s;                       // 翻转
        } else if (b.lots.isEmpty()) {
            b.dir = 0;
        }
    }

    public Position get(String symbol) {
        Book b = books.get(symbol);
        if (b == null) return Position.flat(symbol);
        long qty = 0, cost = 0;
        for (Lot l : b.lots) {
            qty += l.qty;
            cost = Math.addExact(cost, Math.multiplyExact(l.qty, l.px));
        }
        return new Position(symbol, b.dir * qty, cost, b.realized);
    }

    public long netQty(String symbol) {
        Book b = books.get(symbol);
        if (b == null) return 0;
        long qty = 0;
        for (Lot l : b.lots) qty += l.qty;
        return b.dir * qty;
    }

    public long totalRealized() {
        long t = 0;
        for (Book b : books.values()) t = Math.addExact(t, b.realized);
        return t;
    }

    /** 所有出现过的标的，字典序。 */
    public List<String> symbols() { return books.keySet().stream().sorted().toList(); }
}
