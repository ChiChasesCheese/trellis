"""Applicants who look like nodes of one campaign: the same operators apply under different names.

Two applicants are linked when they overlap on at least ``correlation.min_overlap_kinds`` *kinds* of
value (phone block, IP /24, resume fingerprint, email). One shared value alone is common (an office
NAT, a recruiting agency's phone) and is not evidence. All comparison goes through normalize.py,
and only within the tenant: cross-tenant correlation is a contract question, not a v1 feature.
"""
from __future__ import annotations

import ipaddress
from collections import defaultdict

from vetting import normalize
from vetting.models import Finding, Kind, Observation
from vetting.signals.base import Signal, SignalContext, register_signal

Keys = dict[str, dict[str, list[Observation]]]  # family -> key -> observations that produced it

_KINDS = (Kind.PHONE, Kind.IP, Kind.LOGIN_IP, Kind.EMAIL, Kind.RESUME_SHA256, Kind.RESUME_AUTHOR, Kind.RESUME_TOOL)


def _keys(observations: list[Observation], digits: int, allow: list[ipaddress.IPv4Network | ipaddress.IPv6Network]) -> Keys:
    keys: Keys = defaultdict(lambda: defaultdict(list))
    by_kind: dict[Kind, list[Observation]] = defaultdict(list)
    for obs in observations:
        by_kind[obs.kind].append(obs)
    for obs in by_kind[Kind.PHONE]:
        if e164 := normalize.phone_e164(obs.value):
            keys["phone"][normalize.phone_prefix(e164, digits)].append(obs)
    for obs in [*by_kind[Kind.IP], *by_kind[Kind.LOGIN_IP]]:
        prefix = normalize.ip_prefix24(obs.value)
        if prefix and not any(ipaddress.ip_address(obs.value) in net for net in allow if net.version == ipaddress.ip_address(obs.value).version):
            keys["ip"][prefix].append(obs)
    for obs in by_kind[Kind.EMAIL]:
        if key := normalize.email_key(obs.value):
            keys["email"][key].append(obs)
    for obs in by_kind[Kind.RESUME_SHA256]:
        keys["resume"][f"sha256:{obs.value.lower()}"].append(obs)
    for author in by_kind[Kind.RESUME_AUTHOR]:
        for tool in by_kind[Kind.RESUME_TOOL]:
            if name := normalize.name_key(author.value):
                keys["resume"][f"author+tool:{name}|{tool.value.casefold()}"].extend([author, tool])
    return keys


@register_signal
class CoordinatedApplicants(Signal):
    name = "coordinated_applicants"

    def evaluate(self, ctx: SignalContext) -> Finding | None:
        cfg = ctx.settings.correlation
        allow = [ipaddress.ip_network(cidr) for cidr in cfg.allowlist_cidrs]
        mine = _keys(ctx.observations, cfg.phone_prefix_digits, allow)
        if not mine:
            return None
        others: dict[str, list[Observation]] = defaultdict(list)
        for kind in _KINDS:
            for obs in ctx.store.observations.list_by_kind(ctx.identity.tenant_id, kind):
                if obs.identity_id != ctx.identity.id:
                    others[obs.identity_id].append(obs)

        linked: dict[str, set[str]] = {}
        evidence: list[Observation] = []
        for other_id, observations in sorted(others.items()):
            theirs = _keys(observations, cfg.phone_prefix_digits, allow)
            families = {fam for fam, table in mine.items() if set(table) & set(theirs.get(fam, {}))}
            if len(families) < cfg.min_overlap_kinds:
                continue
            linked[other_id] = families
            for fam in families:
                for key in set(mine[fam]) & set(theirs[fam]):
                    evidence.extend(mine[fam][key])
                    evidence.extend(theirs[fam][key])
        if not linked:
            return None
        detail = "; ".join(f"{other} via {', '.join(sorted(fams))}" for other, fams in linked.items())
        unique = list({(o.identity_id, o.raw_ref): o for o in evidence}.values())
        return self.finding(
            ctx, f"Overlaps with {len(linked)} other applicant(s) on multiple kinds of identifier: {detail}", unique
        )
