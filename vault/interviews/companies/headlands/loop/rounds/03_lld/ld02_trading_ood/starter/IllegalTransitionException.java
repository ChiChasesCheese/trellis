/** 事件对当前状态不合法（例如 FILLED 之后又来 Fill、超量成交、成交价越过限价）。抛出时订单状态不变。 */
public class IllegalTransitionException extends IllegalStateException {
    public IllegalTransitionException(String message) { super(message); }
}
