/**
 * 一套风控限额（所有限额都严格大于 0；恒等于 0 的限额没有意义，只会是配置错误）。
 *
 * @param maxOrderQty      单笔最大数量
 * @param maxOrderNotional 单笔最大名义金额 px*qty（tick * 股）
 * @param maxPosition      单标的最坏情况净仓绝对值上限（含所有未完成订单）
 * @param maxOpenOrders    全账户同时未完成订单数上限
 * @param priceBandBps     价格带：|px - 参考价| / 参考价 不得超过多少个基点（1 bp = 0.01%）。「胖手指」防护
 */
public record RiskLimits(long maxOrderQty, long maxOrderNotional, long maxPosition, int maxOpenOrders, long priceBandBps) {
    public RiskLimits {
        if (maxOrderQty <= 0 || maxOrderNotional <= 0 || maxPosition <= 0 || maxOpenOrders <= 0 || priceBandBps <= 0)
            throw new IllegalArgumentException("all risk limits must be > 0");
    }
}
