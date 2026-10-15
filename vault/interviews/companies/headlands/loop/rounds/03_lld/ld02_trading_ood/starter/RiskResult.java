/** 风控结论：通过，或带原因拒绝。sealed + record：调用方用 switch 模式匹配处理，不会漏分支。 */
public sealed interface RiskResult permits RiskResult.Accepted, RiskResult.Rejected {
    RiskResult ACCEPTED = new Accepted();

    record Accepted() implements RiskResult {}

    record Rejected(RiskReason reason) implements RiskResult {}

    default boolean isAccepted() { return this instanceof Accepted; }
}
