import java.util.Objects;

/**
 * 限价单。价格用整数 tick（最小报价单位）表示，数量用整数股数——整数没有舍入误差，PnL 才能逐位对上。
 * 紧凑构造器把「不可能的订单」挡在类型外面：之后所有代码都不用再检查 qty > 0。
 */
public record Order(long id, String symbol, Side side, long qty, long px) {
    public Order {
        Objects.requireNonNull(symbol, "symbol");
        Objects.requireNonNull(side, "side");
        if (id <= 0) throw new IllegalArgumentException("id must be > 0: " + id);
        if (symbol.isBlank()) throw new IllegalArgumentException("symbol is blank");
        if (qty <= 0) throw new IllegalArgumentException("qty must be > 0: " + qty);
        if (px <= 0) throw new IllegalArgumentException("px must be > 0: " + px);
    }
}
