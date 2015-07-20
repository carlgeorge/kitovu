import yaml
import appdirs
from .errors import ConfigError


def parse_config(profile):
    config_dir = appdirs.user_config_dir(__package__)
    profile_file = '{}/{}.yaml'.format(config_dir, profile)
    data = safe_yaml_load(profile_file)
    hub = data.get('hub', 'https://api.github.com')
    user = safe_key_retrieve('user', data)
    token = safe_key_retrieve('token', data)
    return hub, user, token


def safe_yaml_load(path):
    with open(path) as f:
        try:
            return yaml.load(f.read())
        except yaml.YAMLError:
            raise ConfigError('error parsing {}'.format(path))


def safe_key_retrieve(want, data):
    try:
        return data[want]
    except KeyError:
        raise ConfigError('missing config parameter "{}"'.format(want))
