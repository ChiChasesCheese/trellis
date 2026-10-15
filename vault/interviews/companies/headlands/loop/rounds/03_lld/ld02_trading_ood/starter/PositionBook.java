import java.util.List;

/**
 * Part 2：仓位与盈亏，FIFO 配对，全整数。
 */
public final class PositionBook {
    /** 一笔成交（我方视角：side = 我方方向）。qty、px 必须 > 0，否则 IllegalArgumentException。 */
    public void onFill(String symbol, Side side, long qty, long px) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 未出现过的标的返回 Position.flat(symbol)。 */
    public Position get(String symbol) {
        throw new UnsupportedOperationException("TODO");
    }

    public long netQty(String symbol) {
        throw new UnsupportedOperationException("TODO");
    }

    public long totalRealized() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 所有出现过的标的，字典序。 */
    public List<String> symbols() {
        throw new UnsupportedOperationException("TODO");
    }
}
