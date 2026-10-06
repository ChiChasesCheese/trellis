from vetting.models import Finding, Kind
from vetting.signals.base import Signal, SignalContext, register_signal


@register_signal
class VpnHostingIp(Signal):
    name = "vpn_hosting_ip"

    def evaluate(self, ctx: SignalContext) -> Finding | None:
        hits = []
        for obs in [*ctx.of(Kind.IP), *ctx.of(Kind.LOGIN_IP)]:
            info = ctx.lookups.ip.lookup(obs.value)
            if info.is_vpn or info.is_hosting:
                hits.append((obs, info))
        if not hits:
            return None
        info = hits[0][1]
        label = "VPN" if info.is_vpn else "hosting"
        return self.finding(
            ctx,
            f"IP address belongs to a {label} network ({info.org}, {info.asn})",
            [obs for obs, _ in hits],
            subject=f"asn:{info.asn}",
        )
