import yaml
from .xdg import get_config_path


def parse_config(profile):
    config_path = get_config_path(__package__)
    profile_path = (config_path / profile).with_suffix('.yaml')
    data = safe_yaml_load(profile_path)
    hub = data.get('hub', 'https://api.github.com')
    user = safe_key_retrieve('user', data)
    token = safe_key_retrieve('token', data)
    return hub, user, token


def safe_yaml_load(path):
    with path.open() as f:
        try:
            return yaml.load(f.read())
        except yaml.YAMLError:
            raise SystemExit('error parsing {}'.format(config_file))


def safe_key_retrieve(want, data):
    try:
        return data[want]
    except KeyError:
        msg = 'missing required config parameter "{}"'
        raise SystemExit(msg.format(want))
