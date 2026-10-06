"""Exception types. Everything we raise on purpose derives from InsiderWatchError."""


class InsiderWatchError(Exception):
    """Base class; the CLI turns these into a one-line message and exit code 2."""


class ConfigError(InsiderWatchError):
    pass


class ConnectorError(InsiderWatchError):
    pass


class RosterError(InsiderWatchError):
    pass
