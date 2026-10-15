/** 对端发来的字节流不符合帧协议（长度为负 / 超过 maxFrame）。不可恢复：流已经失去同步，只能断开重连。 */
public class FrameException extends RuntimeException {
    public FrameException(String message) { super(message); }
}
