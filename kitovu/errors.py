class KitovuError(Exception):
    pass


class ConfigError(KitovuError):
    pass


class MissingConfigError(ConfigError):
    pass
