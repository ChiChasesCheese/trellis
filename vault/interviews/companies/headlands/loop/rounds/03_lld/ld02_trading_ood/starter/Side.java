/** 买卖方向。sign() 让 PositionBook 可以用一套算术处理多头和空头，而不是两份 if/else。 */
public enum Side {
    BUY(+1), SELL(-1);

    private final int sign;

    Side(int sign) { this.sign = sign; }

    /** BUY = +1，SELL = -1。 */
    public int sign() { return sign; }

    public Side opposite() { return this == BUY ? SELL : BUY; }
}
