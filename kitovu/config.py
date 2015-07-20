import yaml
import appdirs
from .errors import ConfigError


def load_profile(profile):
    config_dir = appdirs.user_config_dir(__package__)
    config = '{}/{}.yaml'.format(config_dir, profile)
    return load_config(config)


def load_config(config):
    data = safe_yaml_load(config)
    hub = data.get('hub', 'https://api.github.com')
    token = safe_key_retrieve('token', data)
    return hub, token


def safe_yaml_load(path):
    try:
        with open(path) as f:
            try:
                return yaml.load(f.read())
            except yaml.YAMLError:
                raise ConfigError('{}: yaml error'.format(path))
    except FileNotFoundError:
        raise ConfigError('{}: file does not exist'.format(path))


def safe_key_retrieve(want, data):
    try:
        return data[want]
    except KeyError:
        raise ConfigError('missing config parameter "{}"'.format(want))
