/** 拒绝原因。声明顺序就是检查顺序：同时违反多条时，报告第一条（确定性：replay 必须得到同一个原因）。 */
public enum RiskReason {
    HALTED, NO_REFERENCE_PRICE, QTY_LIMIT, NOTIONAL_LIMIT, PRICE_BAND, OPEN_ORDERS_LIMIT, POSITION_LIMIT
}
