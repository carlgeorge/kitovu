import yaml


def load_profile(profile):
    try:
        import appdirs
    except ModuleNotFoundError:
        raise SystemExit('The appdirs module is required for profile support, but could not be imported.')
    config_dir = appdirs.user_config_dir('github')
    config = f"{config_dir}/{profile}.yaml"
    return load_config(config)


def load_config(config):
    data = safe_yaml_load(config)
    hub = data.get('hub')
    token = data.get('token')
    return hub, token


def safe_yaml_load(path):
    try:
        with open(path) as f:
            try:
                return yaml.load(f.read())
            except yaml.YAMLError:
                raise SystemExit(f"{path}: yaml error")
    except FileNotFoundError:
        raise SystemExit(f"{path}: file does not exist")
