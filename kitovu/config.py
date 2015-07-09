import yaml
import appdirs


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
            raise SystemExit('error parsing {}'.format(path))


def safe_key_retrieve(want, data):
    try:
        return data[want]
    except KeyError:
        msg = 'missing required config parameter "{}"'
        raise SystemExit(msg.format(want))
