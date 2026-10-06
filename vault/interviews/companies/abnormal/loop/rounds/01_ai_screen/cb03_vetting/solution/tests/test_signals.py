from vetting.models import Kind
from vetting.signals import SIGNALS


def run(name, ctx):
    return SIGNALS[name]().evaluate(ctx)


class TestVoipPhone:
    def test_fires_on_voip_number_in_any_format(self, make_ctx):
        finding = run("voip_phone", make_ctx((Kind.PHONE, "+1 (646) 555-0102")))
        assert finding and finding.subject == "phone:+16465550102"
        assert finding.evidence[0].ref == "greenhouse:1#t0"

    def test_quiet_on_mobile_unknown_and_garbage(self, make_ctx):
        assert run("voip_phone", make_ctx((Kind.PHONE, "(212) 555-0101"))) is None
        assert run("voip_phone", make_ctx((Kind.PHONE, "(999) 555-0000"))) is None
        assert run("voip_phone", make_ctx((Kind.PHONE, "555-0143"))) is None


class TestIpGeoMismatch:
    def test_fires_when_ip_country_differs_from_claim(self, make_ctx):
        finding = run("ip_geo_mismatch", make_ctx((Kind.COUNTRY, "US"), (Kind.IP, "192.0.2.140")))
        assert finding and "GB" in finding.summary and len(finding.evidence) == 2

    def test_fires_on_idp_login_country(self, make_ctx):
        assert run("ip_geo_mismatch", make_ctx((Kind.COUNTRY, "US"), (Kind.LOGIN_COUNTRY, "DE")))

    def test_quiet_when_countries_agree_or_claim_missing(self, make_ctx):
        assert run("ip_geo_mismatch", make_ctx((Kind.COUNTRY, "US"), (Kind.IP, "192.0.2.10"))) is None
        assert run("ip_geo_mismatch", make_ctx((Kind.IP, "192.0.2.140"))) is None


class TestResumeNameMismatch:
    def test_fires_on_different_names(self, make_ctx):
        finding = run("resume_name_mismatch", make_ctx((Kind.NAME, "Riley Sample"), (Kind.RESUME_NAME, "Ryley Sampler")))
        assert finding and "Ryley Sampler" in finding.summary

    def test_accents_case_and_order_are_not_a_mismatch(self, make_ctx):
        ctx = make_ctx((Kind.NAME, "Zoë Testwood"), (Kind.RESUME_NAME, "Testwood, Zoe"))
        assert run("resume_name_mismatch", ctx) is None


class TestDisposableEmail:
    def test_fires_on_disposable_domain(self, make_ctx):
        finding = run("disposable_email", make_ctx((Kind.EMAIL, "x@Burner.Example.org")))
        assert finding and finding.subject == "domain:burner.example.org"

    def test_quiet_on_normal_domain(self, make_ctx):
        assert run("disposable_email", make_ctx((Kind.EMAIL, "x@example.com"))) is None


class TestVpnHostingIp:
    def test_fires_and_names_the_asn(self, make_ctx):
        finding = run("vpn_hosting_ip", make_ctx((Kind.IP, "203.0.113.20"), (Kind.LOGIN_IP, "203.0.113.21")))
        assert finding and finding.subject == "asn:AS64500" and len(finding.evidence) == 2

    def test_quiet_on_residential_ip(self, make_ctx):
        assert run("vpn_hosting_ip", make_ctx((Kind.IP, "192.0.2.10"))) is None


def test_every_registered_signal_has_a_weight(settings):
    settings.require_weights(SIGNALS)
