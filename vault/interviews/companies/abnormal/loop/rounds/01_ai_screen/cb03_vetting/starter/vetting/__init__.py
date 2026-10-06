"""vetting: candidate identity vetting for security teams.

Reads applications from an ATS and sign-in logs from an identity provider, runs signals over
them, and produces a per-candidate review for a human security reviewer. It never decides
anything about hiring.
"""

__version__ = "0.4.0"
